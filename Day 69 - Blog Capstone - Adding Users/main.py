import flask
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterNewUserForm, LoginForm
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##Setup Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


##CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    author_account = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "user_accounts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


def is_logged_in():
    return current_user.is_authenticated


@app.route('/')
def get_all_posts():

    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


def login_failed():
    flash("Either this email doesn't exist, or the password entered was incorrect.")


def check_for_existing_user(email):
    """
        Returns true if email is already in database, false if not.
    """
    user = db.session.query(User).filter_by(email=email).first()
    return user is not None


def get_next_page():
    next_page = flask.request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('get_all_posts')

    return next_page


@app.route('/register', methods=['GET', 'POST'])
def register():

    # On the off chance the user typed in the url to register:
    # Check to make sure user isn't already signed in
    if is_logged_in():
        return redirect(url_for('get_all_posts'))

    form = RegisterNewUserForm()
    if form.validate_on_submit():

        if not check_for_existing_user(form.email.data):
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


@app.route('/logout')
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


def check_permissions(post):
    return current_user.email == post.author_account


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


if __name__ == "__main__":
    app.run(debug=True)
