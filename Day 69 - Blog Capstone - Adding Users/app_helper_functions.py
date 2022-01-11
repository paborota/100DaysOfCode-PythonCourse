from app_data import User
from flask import flash, request, url_for
from flask_login import current_user
from werkzeug.urls import url_parse


def login_failed():
    flash("Either this email doesn't exist, or the password entered was incorrect.")


def check_for_existing_user(db, user_class, email):
    """
        Returns true if email is already in database, false if not.
    """
    user = db.session.query(User).filter_by(email=email).first()
    return user is not None


def check_permissions(post):
    return current_user.email == post.author_account


def get_next_page():
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('get_all_posts')

    return next_page


def is_logged_in():
    return current_user.is_authenticated
