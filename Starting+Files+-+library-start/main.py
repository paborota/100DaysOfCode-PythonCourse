from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(250), unique=True, nullable=False)
    author = db.Column(db.VARCHAR(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f"{self.title} - {self.author} - {self.rating}/10"

    def __repr__(self):
        return f"<Title {self.title}>"


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form['book_id']
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect('/')
    book = Book.query.get(request.args.get('book_id'))
    return render_template('edit.html', book=book)


@app.route('/delete')
def delete():
    book_to_delete = Book.query.get(request.args.get('book_id'))
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
