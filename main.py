from flask import Flask, render_template, request, redirect, session, url_for, jsonify

# import custom classes
from user import User
from post import Post

# instantiate objects
app = Flask(__name__)

# instantiate custom objects
my_user = User()
my_post = Post()


@app.route('/')
def root():
    return render_template('index.html')


# user
@app.route('/user', methods=['GET'])
def user_index():
    '''
    List of all users
    '''
    all_users = [
        {
            "name": "farajiii",
            "email": "faraji@gmail.coms"
        },
        {
            "name": "fuji",
            "email": "fuji@gmail.com"
        }
    ]

    return jsonify(all_users)


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


@app.route('/user/<int:id>', methods=['GET'])
def user_show(id):
    '''
    Show a user.
    '''
    pass


@app.route('/user/<int:id>/edit', methods=['GET'])
def user_edit():
    '''
    Form to edit user.
    '''
    pass


@app.route('/user/<int:id>', methods=['PATCH'])
def user_update():
    '''
    Update a user.
    '''
    pass


@app.route('/user/<int:id>', methods=['DELETE'])
def user_delete():
    '''
    Delete a user.
    '''
    pass


# post
@app.route('/post', methods=['GET'])
def post_index():
    '''
    All posts
    '''
    pass


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
    pass


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


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1', port=8080, debug=True)
