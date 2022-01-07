
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


# #CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():

    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        new_user = User(
            name=request.form.get('name').title(),
            email=request.form.get('email'),
            password=request.form.get('password')
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

            if user.password == request.form.get('password'):

                return render_template('secrets.html', user=user)

            else:

                login_failed()
        else:

            login_failed()

    return render_template("login.html")


def login_failed():

    flash("This account either doesn't exist, or the password is incorrect.")


@app.route('/secrets')
def secrets():

    return render_template("secrets.html")


@app.route('/logout')
def logout():

    pass


@app.route('/download/<filename>', methods=['GET'])
def download(filename):

    return send_from_directory(f"{app.static_folder}/files", filename=filename, as_attachment=True)


if __name__ == "__main__":

    app.run(debug=True)
