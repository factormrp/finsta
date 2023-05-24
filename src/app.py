from flask import Flask, render_template, request, jsonify
from sqlalchemy.orm import sessionmaker
from models.base_model import BaseModel
from analyze import get_user_from_file
from sqlalchemy import create_engine
from models.user import User
import json
import os

# instantiate app and configure it
app =  Flask(__name__)
app.config.from_file('config.json', load=json.load)
app.static_folder = 'static'


# instantiate engine and create local sessionmaker
engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    connect_args={'check_same_thread': False}
)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# setup demo database
@app.before_first_request
def setup():
    # Recreate database each time for demo
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)

    # Get the directory path of the app.py file
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    outputs_dir = os.path.join(app_dir, 'outputs')

    # Iterate over files in the outputs folder
    for file_name in os.listdir(outputs_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(outputs_dir, file_name)
            try:
                # Extract user data from the file
                user = get_user_from_file(file_path)
                # Add user data to the database
                with LocalSession.begin() as sesh:
                    sesh.add(User(
                        name = user[0],
                        followers = user[1],
                        following = user[2],
                        posts = user[3]
                    ))
            except ValueError:
                print(f"Failed to load data from file: {file_path}")


@app.route('/sort_users')
def sort_users():
    sort_by = request.args.get('sort_by')

    with LocalSession.begin() as sesh:
        if sort_by == 'username':
            users = sesh.query(User).order_by(User.name).all()
        elif sort_by == 'following':
            users = sesh.query(User).order_by(User.following.desc()).all()
        elif sort_by == 'followers':
            users = sesh.query(User).order_by(User.followers.desc()).all()
        elif sort_by == 'posts':
            users = sesh.query(User).order_by(User.posts.desc()).all()
        else:
            users = sesh.query(User).all()

        sesh.expunge_all()

    return render_template('user_list.html', users=users)


@app.route('/')
def root():
    with LocalSession.begin() as sesh:
        users = sesh.query(User).all()
        sesh.expunge_all()

    return render_template('user_list.html', users=users)


# TODO:
# Add favicon handler
# Add general error handler
# Add logger
# Add event listeners
# Add components for event listeners

# PFR:
# Display user list of followers
# Display user list of following
# Display visualization of full personal social graph


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
