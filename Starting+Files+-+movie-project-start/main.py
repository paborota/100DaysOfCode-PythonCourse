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
    description = db.Column(db.String(900), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(800), nullable=False)
    img_url = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


class MovieDBInterface():

    API_KEY = "dad2dfd78877900ed13e607c0a3731d5"
    DB_URL = "https://api.themoviedb.org/3/"

    def query_movie_name(self, movie_name):

        url = self.DB_URL + "search/movie/"
        # response = requests.get(self.DB_URL, params=params, headers=headers)
        response = requests.get(url, params={'api_key': self.API_KEY, 'query': movie_name})

        return response.json()['results']

    def find_movie(self, movie_id):

        url = self.DB_URL + f"movie/{movie_id}"
        response = requests.get(url, params={'api_key': self.API_KEY})

        return response.json()


class RatingForm(FlaskForm):

    rating = DecimalField(u'Your Rating out of 10 e.g. 7.5')
    review = StringField(u'Your Review')
    submit_button = SubmitField(u'Submit')

class AddForm(FlaskForm):

    title = StringField(u'Movie Title')
    submit_button = SubmitField(u'Submit')


class EditForm(FlaskForm):

    rating = DecimalField(u'Your Rating out of 10 e.g. 7.5', places=1, validators=[validators.number_range(min=0.0, max=10.0)])
    review = StringField(u'Your Review')
    submit_button = SubmitField(u'Save')


@app.route("/add_movie/<movie_id>")
def add_movie(movie_id):

    movie_interface = MovieDBInterface()
    movie_data = movie_interface.find_movie(movie_id)

    movie_to_add = Movie(
        title=movie_data['original_title'],
        year=movie_data['release_date'].split('-')[0],
        description=movie_data['overview'],
        rating=0,
        review='',
        img_url="https://image.tmdb.org/t/p/w500" + movie_data['backdrop_path']
    )

    form = RatingForm(request.form)
    return render_template('add.html', page_type='form', form=form, movie_data=movie_data)


@app.route("/add", methods=['GET', 'POST'])
def add():

    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        movie_interface = MovieDBInterface()
        movies = movie_interface.query_movie_name(request.form.get('title'))

        return render_template("add.html", page_type='list', movies=movies)

    return render_template("add.html", page_type='form', form=form)


@app.route("/delete")
def delete():
    global current_movie_ranking

    movie_to_delete = Movie.query.filter_by(ranking=current_movie_ranking).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(f"/{current_movie_ranking}")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    global current_movie_ranking

    form = EditForm(request.form)
    current_movie = Movie.query.filter_by(rankint=current_movie_ranking).first()
    if request.method == 'POST' and form.validate():
        current_movie.rating = request.form.get('rating')
        current_movie.review = request.form.get('review')
        db.session.commit()
        return redirect(f'/{current_movie.id}')

    return render_template("edit.html", movie=current_movie, form=form)


@app.route("/<movie_ranking>")
def movie(movie_ranking: int):
    global current_movie_ranking

    current_movie = Movie.query.filter_by(ranking=movie_ranking).first()
    if current_movie is None:
        current_movie = ''
        current_movie_ranking = 1
    else:
        current_movie_ranking = current_movie.ranking
    return render_template("index.html", movie=current_movie)


@app.route("/")
def home():

    return redirect("/10")


if __name__ == '__main__':
    current_movie_ranking = ''
    app.run(debug=True)
