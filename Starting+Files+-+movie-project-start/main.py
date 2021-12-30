from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, validators
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-rating-collection.db"
db = SQLAlchemy(app)
Bootstrap(app)


class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(800), nullable=False)
    img_url = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


class AddForm(FlaskForm):

    title = StringField(u'Movie Title')
    year = DecimalField(u'Year Released')
    description = StringField(u'Movie Decription')
    rating = DecimalField(u'Your Rating')
    review = StringField(u'Your Review')
    img_url = StringField(u'Link to Image')


class EditForm(FlaskForm):

    rating = DecimalField(u'Your Rating out of 10 e.g. 7.5', places=1, validators=[validators.number_range(min=0.0, max=10.0)])
    review = StringField(u'Your Review')
    submit_button = SubmitField(u'Save')


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddForm(request.form)
    if request.method == 'POST':
        movie_to_add = Movie(
            title = request.form.get('title'),
            year = request.form.get('year'),
            description = request.form.get('description'),
            rating = request.form.get('rating'),
            review = request.form.get('review'),
            img_url = request.form.get('img_url')
        )
        db.session.add(movie_to_add)
        db.session.commit()
        return redirect(f"/{}")

    return render_template("add.html", form=form)


@app.route("/delete")
def delete():
    global current_movie_id

    movie_to_delete = Movie.query.get(current_movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(f"/{current_movie_id}")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    global current_movie_id

    form = EditForm(request.form)
    current_movie = Movie.query.get(current_movie_id)
    if request.method == 'POST' and form.validate():
        current_movie.rating = request.form.get('rating')
        current_movie.review = request.form.get('review')
        db.session.commit()
        return redirect(f'/{current_movie.id}')

    return render_template("edit.html", movie=current_movie, form=form)


@app.route("/<movie_id>")
def movie(movie_id: int):
    global current_movie_id

    current_movie = Movie.query.filter_by(id=movie_id).first()
    if type(current_movie) == 'NoneType':
        return redirect("/add")
    current_movie_id = current_movie.id
    return render_template("index.html", movie=current_movie)


@app.route("/")
def home():
    return redirect("/1")


if __name__ == '__main__':
    current_movie_id = ''
    app.run(debug=True)
