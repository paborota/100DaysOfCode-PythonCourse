from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from movie_interface import MovieDBInterface
from forms import AddForm, EditForm


app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-rating-collection.db"
db = SQLAlchemy(app)
Bootstrap(app)


class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(800), nullable=False)
    img_url = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


def reevaluate_rankings():

    movies = Movie.query.order_by('rating').all()
    i = 1
    for movie in movies[::-1]:

        movie.ranking = i
        i += 1

    db.session.commit()


@app.route("/add_movie/<movie_id>", methods=['GET', 'POST'])
def add_movie(movie_id):

    movie_interface = MovieDBInterface()
    movie_data = movie_interface.find_movie(movie_id)
    selected_movie_release_year = movie_data['release_date'].split('-')[0]

    # Check to see if movie already exists in database
    # First grab the entries that have the same title
    # Then check the entries if they have the same year
    # If they have the same year, assume they are the same movie and ignore
    existing_movies = Movie.query.filter_by(title=movie_data['title']).all()
    for existing_movie in existing_movies:
        if existing_movie.year == int(selected_movie_release_year):
            return redirect(f'/add/{"already exists"}')

    if movie_data['backdrop_path'] is None:
        img_url = '#'
    else:
        img_url = "https://image.tmdb.org/t/p/w500" + movie_data['backdrop_path']

    movie_to_add = Movie(
        title=movie_data['title'],
        year=selected_movie_release_year,
        description=movie_data['overview'],
        rating=0,
        ranking=0,
        review='',
        img_url=img_url
    )

    db.session.add(movie_to_add)
    db.session.commit()
    db.session.refresh(movie_to_add)

    return redirect(f'/edit/{movie_to_add.id}')


@app.route("/select/<movie_title>")
def select(movie_title):

    movie_interface = MovieDBInterface()
    movies = movie_interface.query_movie_name(movie_title)

    return render_template('select.html', movies=movies)


@app.route("/add", methods=['GET', 'POST'])
@app.route("/add/<message>", methods=['GET', 'POST'])
def add(message=''):

    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(f'/select/{request.form.get("title")}')

    can_add = False
    # Check to see if we're already at 10 movies.
    # The list is only up to 10, no more.
    if db.session.query(Movie).count() < 10:
        can_add = True

    return render_template("add.html", form=form, message=message, can_add=can_add)


@app.route("/delete/<movie_id>")
def delete(movie_id):

    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect("/")


@app.route("/edit/<movie_id>", methods=['GET', 'POST'])
def edit(movie_id):

    form = EditForm(request.form)
    current_movie = Movie.query.get(movie_id)

    if request.method == 'POST' and form.validate():
        current_movie.rating = request.form.get('rating')
        current_movie.review = request.form.get('review')
        db.session.commit()

        reevaluate_rankings()

        return redirect('/')

    return render_template("edit.html", movie=current_movie, form=form)


@app.route("/")
def home():

    movies = Movie.query.order_by('rating').all()

    return render_template("index.html", movies=movies, amount_of_movies=len(movies))


if __name__ == '__main__':

    app.run(debug=True)
