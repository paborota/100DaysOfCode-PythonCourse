from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp, URL
import csv


TIME_REGEX = r"^[\d](:\d\d)?[AaPp][Mm]$"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL(require_tld=True, message="This is not a valid URL.")])
    open_time = StringField("Opening Time e.g. 8AM", validators=[DataRequired(), Regexp(TIME_REGEX)])
    closing_time = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired(), Regexp(TIME_REGEX)])
    coffee_rating = SelectField("Coffee Rating", choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "✘"])
    wifi_rating = SelectField("Wifi Strength Rating", choices=["💪", "💪💪", "💪💪💪", "💪💪💪💪", "✘"])
    power_availability = SelectField("Power Socket Availability", choices=["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "✘"])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        with open('cafe-data.csv', 'a', encoding="utf8") as csv_file:
            data_to_append = f"\n{form.cafe.data}," +\
                             f"{form.location.data}," +\
                             f"{form.open_time.data}," +\
                             f"{form.closing_time.data}," +\
                             f"{form.coffee_rating.data}," +\
                             f"{form.wifi_rating.data}," +\
                             f"{form.power_availability.data}"
            csv_file.write(data_to_append)
            return redirect('/cafes')
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
