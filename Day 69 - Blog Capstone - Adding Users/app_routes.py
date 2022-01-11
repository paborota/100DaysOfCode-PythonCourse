from app_data import app, User, BlogPost, db
from app_helper_functions import is_logged_in, login_failed, check_for_existing_user, check_permissions, get_next_page
from datetime import date
from flask import render_template, redirect, flash, url_for
from flask_login import login_user, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterNewUserForm, LoginForm

from sqlalchemy.orm import relationship
from flask_gravatar import Gravatar


@app.route('/')
def get_all_posts():

    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():

    # On the off chance the user typed in the url to register:
    # Check to make sure user isn't already signed in
    if is_logged_in():
        return redirect(url_for('get_all_posts'))

    form = RegisterNewUserForm()
    if form.validate_on_submit():

        if not check_for_existing_user(db=db, user_class=User, email=form.email.data):
            new_user = User(
                email=form.email.data,
                name=form.name.data
            )
            new_user.set_password(form.password.data)

            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)

            login_user(new_user)

            return redirect(get_next_page())
        else:
            flash('This email is already in use.')

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is not None:

            if user.check_password(form.password.data):
                login_user(user)

                return redirect(get_next_page())
            else:
                login_failed()
        else:
            login_failed()

    return render_template("login.html", form=form)


@app.route('/logout', methods=['GET'])
def logout():

    # If we're not logged in, redirect to main page.
    # Wouldn't make sense to logout when already logged out.
    if not is_logged_in():
        return redirect(url_for('get_all_posts'))

    logout_user()

    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>")
def show_post(post_id):

    requested_post = db.session.query(BlogPost).get(post_id)

    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():

    return render_template("about.html")


@app.route("/contact")
def contact():

    return render_template("contact.html")


@app.route("/new-post", methods=['GET', 'POST'])
@login_required
def add_new_post():

    form = CreatePostForm()
    if form.validate_on_submit():

        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user.name,
            author_account=current_user.email,
            date=date.today().strftime("%B %d, %Y")
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>")
@login_required
def edit_post(post_id):

    post = db.session.query(BlogPost).get(post_id)

    if not check_permissions(post):
        # flash('You do not have permissions to edit this post.')
        return redirect(url_for('get_all_posts'))

    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():

        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data

        db.session.commit()

        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):

    post_to_delete = db.session.query(BlogPost).get(post_id)

    if check_permissions(post_to_delete):
        db.session.delete(post_to_delete)
        db.session.commit()
    # else:
    #     This user lacks permissions to delete the post.
    #     flash('You cannot perform this action.')

    return redirect(url_for('get_all_posts'))
