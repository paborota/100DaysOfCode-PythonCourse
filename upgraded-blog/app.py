from flask import Flask, render_template, request
import requests
import smtplib


EMAIL_SMTP = "smtp.gmail.com"
EMAIL = "paulborota9@gmail.com"
PASSWORD = "hentaI#42"


app = Flask(__name__)

response = requests.get("https://api.npoint.io/a8d9df49db6a83d1e253")
data = response.json()

imgs = ['cactus.jpg', 'clock.jpg', 'bread.jpg']


def send_email(name, email, phone, message):
    with smtplib.SMTP(EMAIL_SMTP) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL,
                            to_addrs=EMAIL,
                            msg=f"Subject:CONTACT FORM\n\n"
                                f"Name: {name}\n"
                                f"Email: {email}\n"
                                f"Phone: {phone}\n"
                                f"Message: {message}\n")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    msg_sent = False

    if request.method == "POST":
        send_email(request.form["name"], request.form["email"], request.form["phone"], request.form["message"])
        msg_sent = True

    return render_template("contact.html", msg_sent=msg_sent)


@app.route('/post/<int:post_id>')
def post(post_id):
    global data
    global imgs

    if post_id == 0:
        return render_template("sample-post.html")

    i = 0
    for post in data:
        if post['id'] == post_id:
            return render_template("post.html", post=post, img=imgs[i])
        i += 1


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/')
def home():  # put application's code here
    global data
    return render_template("index.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
