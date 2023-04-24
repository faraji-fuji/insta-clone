from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from google.cloud import datastore
from google.cloud import storage
from google.auth.transport import requests
from pprint import pprint
import datetime
import google.oauth2.id_token
import local_constants

# instantiate objects
app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()
storage_client = storage.Client(project=local_constants.PROJECT_NAME)
bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)


@app.route('/')
def root():
    id_token = request.cookies.get("token")
    user_entity = None
    user_id = None

    if id_token:
        try:
            # verify id token
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            user_id = claims['user_id']
            user_key = datastore_client.key('User', user_id)

            # get user entity
            user_entity = datastore_client.get(user_key)

            if user_entity == None:
                # create user
                entity = datastore.Entity(key=user_key)
                entity.update({
                    'setup': 0
                })
                datastore_client.put(entity)

                # get created user
                user_entity = datastore_client.get(user_key)

            if not user_entity['setup']:
                url = f"/user/{user_id}/edit"
                return redirect(url)

            # session['user_entity'] = user_entity
            session['user_id'] = claims['user_id']

        except ValueError as exc:
            error_message = str(exc)
    return render_template('index.html', user_entity=user_entity, user_id=user_id)

##############################################################################
# user routes
##############################################################################


@app.route('/user/<string:user_id>', methods=['GET'])
def user_show(user_id):
    ''' Show a user (profile).

    :param user_id: The identifier of the user.
    :return: Render template profile page with minimal data.
    '''
    return render_template("profile.html", user_id=user_id)


@app.route('/api/user/<string:user_id>', methods=['GET'])
def api_user_show(user_id):
    ''' Get user profile data.

    :param user_id: The identifier of the user.
    '''
    is_following = None

    user_key = datastore_client.key("User", user_id)
    user_entity = datastore_client.get(user_key)

    # get profile page statistics
    following = len(user_entity['following'])
    followers = len(user_entity['followers'])
    posts = len(user_entity['posts'])

    # check if the user_id belongs to the current user
    current_user = user_id == session["user_id"]

    # check following status
    if session["user_id"] in user_entity['followers']:
        is_following = True
    else:
        is_following = False

    data = {
        "following": following,
        "followers": followers,
        "posts": posts,
        "current_user": current_user,
        "is_following": is_following,
        "profile_name": user_entity['profile_name'],
        "username": user_entity['username']}

    return jsonify(data)


@app.route('/api/user/<string:profile_name>/search')
def user_search(profile_name):
    ''' Search a user by profile name

    :param profile_name: The profile name to search.
    :return: An array containing the search results.
    '''
    results = []

    query = datastore_client.query(kind="User")
    query.projection = ['profile_name']
    user_entities = query.fetch()

    for user_entity in user_entities:
        if profile_name in user_entity['profile_name']:
            results.append({
                "user_id": user_entity.key.id_or_name,
                "profile_name": user_entity['profile_name']
            })
    return jsonify(results)


@app.route('/user/<string:user_id>/edit', methods=['GET'])
def user_edit(user_id):
    ''' Form to edit user.

    :param user_id: The identifier of the user.
    '''
    user_key = datastore_client.key('User', user_id)
    user_entity = datastore_client.get(user_key)
    return render_template('user_edit_form.html', user_entity=user_entity)


@app.route('/user/<string:user_id>/edit', methods=['POST'])
def user_update(user_id):
    ''' Update a user. 

    :param user_id: The identifier of the user to update.
    :return: Redirect to home route.
    '''
    username = request.form['username']
    profile_name = request.form['profile_name']

    user_key = datastore_client.key('User', user_id)
    user_entity = datastore_client.get(user_key)
    user_entity.update({
        'username': username,
        'profile_name': profile_name,
        'setup': 1,
        'following': [],
        'followers': [],
        'posts': [],
        'date_created': datetime.datetime.now()
    })
    datastore_client.put(user_entity)
    return redirect("/")


@app.route('/api/user/<string:follow_user_id>/follow', methods=['POST'])
def user_update_follow(follow_user_id):
    ''' Follow a user.

    :param follow_user_id: The identifier of the user to follow.
    '''
    # get entities involved
    user_id = session['user_id']
    user_key = datastore_client.key("User", user_id)
    user_entity = datastore_client.get(user_key)

    follow_user_key = datastore_client.key("User", follow_user_id)
    follow_user_entity = datastore_client.get(follow_user_key)

    # add follow_user_id to the current user's following list
    following = user_entity['following']

    if follow_user_id not in following:
        following.append(follow_user_id)
        user_entity.update({
            'following': following
        })

        # add user_id to followers list of the account being followed
        followers = follow_user_entity['followers']
        followers.append(user_id)
        follow_user_entity.update({
            'followers': followers
        })

        # commit the changes as a transaction
        transaction = datastore_client.transaction()
        with transaction:
            transaction.put(user_entity)
            transaction.put(follow_user_entity)

    return "success", 201


@app.route('/api/user/<string:unfollow_user_id>/unfollow', methods=['POST'])
def user_update_unfollow(unfollow_user_id):
    ''' Unfollow a user.

    :param unfollow_user_id: The identifier of the user to unfollow.
    '''
    # get involved entities
    user_id = session['user_id']
    user_key = datastore_client.key('User', user_id)
    user_entity = datastore_client.get(user_key)

    unfollow_user_key = datastore_client.key("User", unfollow_user_id)
    unfollow_user_entity = datastore_client.get(unfollow_user_key)

    # remove follow_user_id to the current user's following list
    following = user_entity['following']
    if unfollow_user_id in following:
        following.remove(unfollow_user_id)
        user_entity.update({
            'following': following
        })

        # remove user_id to followers list of the account being followed
        followers = unfollow_user_entity['followers']
        followers.remove(user_id)
        unfollow_user_entity.update({
            'followers': followers
        })

        # commit the changes as a transaction
        transaction = datastore_client.transaction()
        with transaction:
            transaction.put(user_entity)
            transaction.put(unfollow_user_entity)

    return "success", 200


@app.route('/user/<string:user_id>/following')
def user_following(user_id):
    ''' Get following list

    :param user_id: The identifier of the user whose followers we are getting.
    :return: Following list template with minimal data.
    '''
    return render_template("following.html", user_id=user_id)


@app.route('/api/user/<string:user_id>/following')
def api_user_following(user_id):
    ''' Get following list data.

    :param user_id: The identifier of the user whose followers we are getting.
    :return: A list of user entities that follow the user identified above. 
    '''
    key = datastore_client.key('User', user_id)
    user = datastore_client.get(key)
    following = user['following']

    following_keys = []
    for follow in following:
        follow_key = datastore_client("User", follow)
        following_keys.append(follow_key)

    following_entities = datastore_client.get_multi(following_keys)

    return jsonify(following_entities)


@app.route('/user/<string:user_id>/followers')
def user_followers(user_id):
    ''' Get follower list

    :user_id: The identifier of the user.
    :return: Template page with minimal data.
    '''
    return render_template("followers.html", user_id=user_id)


@app.route('/api/user/<string:user_id>/followers')
def api_user_followers(user_id):
    ''' Get follower list data.

    :param user_id: The identifier of the user.
    :return: A list of entities that follow the user identified above.
    '''
    key = datastore_client.key('User', user_id)
    user = datastore_client.get(key)
    followers = user['followers']

    follower_keys = []
    for follower in followers:
        follower_key = datastore_client.key("User", follower)
        follower_keys.append(follower_key)

    follower_entities = datastore_client.get_multi(follower_keys)

    return jsonify(follower_entities)


##############################################################################
# Post routes
##############################################################################


@app.route('/api/post/<string:user_id>')
def api_post_index(user_id):
    ''' Get all posts of the associated user_id and return a json response.

    :param user_id: The identifier of the user whose posts we are getting.
    '''
    ancestor_key = datastore_client.key('User', user_id)
    query = datastore_client.query(kind='Post', ancestor=ancestor_key)
    query.order = ['-date_created']
    posts = query.fetch()

    my_posts = []
    for post in posts:
        my_posts.append(post)

    return jsonify(my_posts)


@app.route('/api/post/timeline')
def api_post_user_timeline():
    ''' Get timeline posts. '''
    # get user id from session
    user_id = session["user_id"]
    result = None
    queries = []
    results = []

    # get following list
    my_key = datastore_client.key("User", user_id)
    my_entity = datastore_client.get(my_key)
    following = my_entity['following']
    following.append(user_id)

    # get posts from each person you follow, including yourself
    if following:
        for id in following:
            query = datastore_client.query(kind='Post')
            query.add_filter("publisher", "=", id)
            queries.append(query)

        for query in queries:
            result = query.fetch()
            for item in result:
                item["post_id"] = item.key.id_or_name
                results.append(item)

        # sort the posts by date_created
        results.sort(key=lambda x: x["date_created"], reverse=True)

    # return the first 50 items
    return jsonify(results[:50])


@app.route('/post', methods=['POST'])
def post_create():
    ''' Create a new post. '''
    user_id = session['user_id']

    # get file and caption uploaded from the browser
    file = request.files['file_name']
    caption = request.form['caption']

    # upload file to cloud storage, get public image url
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    blob.make_public()
    image_url = blob.public_url

    # create a post entity
    # my_post.create_post(user_id, caption, image_url)
    post_key = datastore_client.key('User', user_id, 'Post')
    post_entity = datastore.Entity(post_key)
    post_entity.update({
        'likes': 0,
        'publisher': user_id,
        'comments': [],
        'caption': caption,
        'image_url': image_url,
        'date_created': datetime.datetime.now()
    })
    datastore_client.put(post_entity)

    url = f"/user/{session['user_id']}"
    return redirect(url)


@app.route('/api/post/<int:post_id>/<string:user_id>/comment', methods=['POST'])
def api_post_comment(post_id, user_id):
    ''' Comment on a post.

    :param post_id: The identifier of the post.
    :param user_id: The identifier of the user who posted the post.
    '''
    key = datastore_client.key('User', user_id, 'Post', post_id)
    post = datastore_client.get(key)

    comments = post['comments']
    comments.append({
        "publisher": session['user_id'],
        "comment": request.form['comment'],
        "date_created": datetime.datetime.now()
    })

    post.update({
        "comments": comments
    })
    datastore_client.put(post)

    return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1', port=8080, debug=True)
