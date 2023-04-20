from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from google.cloud import datastore
from google.cloud import storage
from google.auth.transport import requests
from pprint import pprint
import datetime
import google.oauth2.id_token



# import custom classes
from user import User
from post import Post
import local_constants

# instantiate objects
app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

storage_client = storage.Client(project=local_constants.PROJECT_NAME)
bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)


# instantiate custom objects
my_user = User()
my_post = Post()


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
            user_entity = my_user.get_user(user_id)

            if user_entity == None:
                my_user.create_user(user_id)
                user_entity = my_user.get_user(user_id)

            if not user_entity['setup']:
                url = f"/user/{user_id}/edit"
                return redirect(url)

            # session['user_data'] = user_data
            session['user_entity'] = user_entity
            session['user_id'] = claims['user_id']

        except ValueError as exc:
            error_message = str(exc)
    return render_template('index.html', user_entity=user_entity, user_id=user_id)

# user resource routes


@app.route('/user', methods=['GET'])
def user_index():
    '''
    List of all users
    '''
    pass

@app.route('/user/new', methods=['GET'])
def user_new():
    '''
    Form to create a new user
    '''
    pass


@app.route('/user', methods=['POST'])
def user_create():
    '''
    Create new user.
    '''
    pass


@app.route('/user/<string:id>', methods=['GET'])
def user_show(id):
    '''
    Show a user (profile).
    '''
    return render_template("profile.html", user_id=session['user_id'])


@app.route('/api/user/<string:id>', methods=['GET'])
def user_show_api(id):
    '''
    Show a user (profile).
    '''
    user_key = datastore_client.key("User", id)
    user_entity = datastore_client.get(user_key)

    following = len(user_entity['following'])
    followers = len(user_entity['followers'])
    posts = len(user_entity['posts'])
    current_user = id == session["user_id"]

    data = {
        "following": following,
        "followers": followers,
        "posts": posts,
        "current_user": current_user,
        "profile_name": user_entity['profile_name'],
        "username": user_entity['username']}

    return jsonify(data)

@app.route('/api/user/<string:profile_name>/search')
def user_search(profile_name):
    results = []

    query = datastore_client.query(kind = "User")
    query.projection = ['profile_name']
    user_entities = query.fetch()

    for user_entity in user_entities:
        if profile_name in user_entity['profile_name']:
            results.append({
                "user_id": user_entity.key.id_or_name,
                "profile_name":user_entity['profile_name']
            })
    return jsonify(results)


@app.route('/user/<string:user_id>/edit', methods=['GET'])
def user_edit(user_id):
    '''
    Form to edit user.
    '''
    user_key = datastore_client.key('User', user_id)
    user_entity = datastore_client.get(user_key)
    return render_template('user_edit_form.html', user_entity=user_entity)


@app.route('/user/<string:user_id>/edit', methods=['POST'])
def user_update(user_id):
    '''
    Update a user.
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
    ''' Follow a user. '''
    user_id = session['user_id']
    my_user.follow_user(user_id, follow_user_id)
    return "success", 201
    
@app.route('/api/user/<string:unfollow_user_id>/unfollow', methods=['POST'])
def user_update_unfollow(unfollow_user_id):
    ''' Unfollow a user. '''
    user_id = session['user_id']
    my_user.unfollow_user(user_id, unfollow_user_id)
    return "success", 200

@app.route('/user/<int:id>', methods=['DELETE'])
def user_delete():
    '''
    Delete a user.
    '''
    pass


@app.route('/api/user/id', methods=['GET'])
def api_user_id():
    data = {}
    data['user_id'] = session["user_id"]
    return jsonify(data)


@app.route('/user/<string:id>/following')
def user_following(id):
    return render_template("following.html")


@app.route('/user/<string:id>/followers')
def user_followers(id):
    return render_template("followers.html")


##############################################################################
# Post routes
##############################################################################


@app.route('/post', methods=['GET'])
def post_index():
    '''
    All posts of a user
    '''
    return jsonify([1, 2, 3, 4, 5])


@app.route('/api/post')
def  api_post_index():
    '''
    Get all posts of the current user and return a json response.
    '''
    user_id = session['user_id']
    posts = my_post.get_posts(user_id)
    my_posts = []

    for post in posts:
        my_posts.append(post)

    return jsonify(my_posts)


@app.route('/post/new', methods=['GET'])
def post_new():
    '''
    Form to create a new post.
    '''
    pass


@app.route('/post', methods=['POST'])
def post_create():
    '''
    Create a new post
    '''
    # get user id from session
    user_id = session['user_id']

    #get file and caption uploaded from the browser 
    file = request.files['file_name']
    caption = request.form['caption']

    # upload file to cloud storage, get public url
    image_url = my_post.upload_file(file)

    #create a post entity 
    my_post.create_post(user_id, caption, image_url)

    url = f"/user/{session['user_id']}"
    return redirect(url)


@app.route('/post/<int:id>', methods=['GET'])
def post_show(id):
    '''
    Show a post
    '''
    pass


@app.route('/post/<int:id>/edit', methods=['GET'])
def post_edit(id):
    '''
    Edit a post.
    '''
    pass


@app.route('/post/<int:id>', methods=['PATCH'])
def post_update(id):
    '''
    Update a post.
    '''
    pass


@app.route('/post/<int:id>', methods=['DELETE'])
def post_delete():
    '''
    Delete a post.
    '''
    pass


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1', port=8080, debug=True)
