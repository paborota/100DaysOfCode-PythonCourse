import flask
from flask import Flask, flash, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
# app.config['DOWNLOAD_FOLDER'] = 'static/files'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


# #CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


# Line below only required once, when creating DB.
# db.create_all()


def verify_user_logged_in():
    return current_user.is_authenticated


@app.route('/')
def home():

    if current_user.is_authenticated:
        return redirect(url_for('secrets'))

    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        hashed_password = generate_password_hash(
            password=request.form.get('password'),
            method="pbkdf2:sha256",
            salt_length=8
        )

        new_user = User(
            name=request.form.get('name').title(),
            email=request.form.get('email'),
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created.')

        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        user = db.session.query(User).filter_by(email=request.form.get('email')).first()
        if user is not None:
            # The user was found in the DB
            # - Verify password entered matches password for user.
            if verify_password(user, request.form.get('password')):
                # Password matched
                # - Login the user.

                login_user(user)

                # flash("Logged in successfully.")

                return redirect(url_for('secrets'))

            else:
                # Passwords did not match
                # - Alert that the login attempt failed.
                # - Then allow the website to load the login page again.
                login_failed()
        else:
            # The email entered could not be found in the DB
            # - Alert that the login attempt failed.
            # - Then allow the website to load the login page again.
            login_failed()

    return render_template("login.html")


def verify_password(user, password):

    return check_password_hash(user.password, password)


def login_failed():

    flash("This account either doesn't exist, or the password is incorrect.")


@app.route('/secrets')
def secrets():

    if not verify_user_logged_in():
        tried_access_without_auth()
        return redirect(url_for('login'))

    return render_template("secrets.html")


@app.route('/logout')
def logout():

    if not verify_user_logged_in():
        flash('You need to be logged in to log out.')
        return redirect(url_for('login'))

    logout_user()
    flash('Logged out successfully.')

    return redirect(url_for('login'))


@app.route('/download/<filename>', methods=['GET'])
def download(filename):

    if not verify_user_logged_in():
        tried_access_without_auth()
        return redirect(url_for('login'))

    return send_from_directory(f"{app.static_folder}/files", filename=filename, as_attachment=True)


def tried_access_without_auth():
    flash('You need to be logged in to access that resource.')


if __name__ == "__main__":

    app.run(debug=True)
