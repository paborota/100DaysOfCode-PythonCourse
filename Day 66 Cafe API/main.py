
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy


API_KEY = "12345qwert"


app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"<{self.name}>"

    def to_dict(self):

        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)

        return dictionary


@app.route("/random", methods=['GET'])
def random():
    from random import choice

    cafes = db.session.query(Cafe).all()
    random_cafe = choice(cafes)

    return jsonify(
        cafe=random_cafe.to_dict()
    )


@app.route("/all", methods=['GET'])
def all():

    cafes = db.session.query(Cafe).all()

    cafes_list = []
    for cafe in cafes:
        cafes_list.append(cafe.to_dict())

    return jsonify(cafes=cafes_list)


@app.route("/search", methods=['GET'])
def search():

    location = request.args.get('location', type=str)
    print(f'Searching for cafes at location: {location}')

    if location is None:
        return cafe_not_found()

    cafes_at_location = db.session.query(Cafe).filter_by(location=location.title()).all()

    list_of_cafes = []
    for cafe in cafes_at_location:
        list_of_cafes.append(cafe.to_dict())

    if len(list_of_cafes) == 0:
        return cafe_not_found()

    # if we got here, we know there is at least 1 cafe found
    return jsonify(
        cafes=list_of_cafes
    ), 200


def cafe_not_found():

    return jsonify(
        error={
            'Not Found': "Sorry, we don't have a cafe at that location."
        }
    ), 404


@app.route("/add", methods=['POST'])
def add():

    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        has_sockets=eval(request.form.get('has_sockets')),
        has_toilet=eval(request.form.get('has_toilet')),
        has_wifi=eval(request.form.get('has_wifi')),
        can_take_calls=eval(request.form.get('can_take_calls')),
        seats=request.form.get('seats'),
        coffee_price=request.form.get('coffee_price')
    )

    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(
        response={
            'success': 'Successfully added the new cafe.'
        }
    ), 200


@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_price(cafe_id):

    cafe_to_patch = db.session.query(Cafe).get(cafe_id)

    if cafe_to_patch is not None:

        cafe_to_patch.coffee_price = request.args.get('coffee_price')
        db.session.commit()

        return jsonify(
            success='Price adjustment was successful.'
        ), 200

    return jsonify(
        error={
            'existential crisis': "That cafe id does not exist."
        }
    ), 404


@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def report_closed(cafe_id):

    if request.headers.get('api_key') != API_KEY:

        return jsonify(
            error={
                'invalid access': 'You do not have the ability to do this action.'
            }
        ), 403

    cafe_to_close = db.session.query(Cafe).get(cafe_id)

    if cafe_to_close is None:

        return jsonify(
            error={
                'existential crisis': 'This cafe id does not exist.'
            }
        ), 404

    db.session.delete(cafe_to_close)
    db.session.commit()

    return jsonify(
        success='Cafe closed successfully.'
    ), 200


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
