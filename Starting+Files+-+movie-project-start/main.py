from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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


@app.route("/<movie_id>")
def movie(movie_id: int):
    movie = Movie.query.filter_by(id=movie_id).first()
    return render_template("index.html", movie=movie)

@app.route("/")
def home():
    return redirect("/1")


if __name__ == '__main__':
    app.run(debug=True)
