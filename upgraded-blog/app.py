from flask import Flask, render_template
import requests

app = Flask(__name__)

response = requests.get("https://api.npoint.io/a8d9df49db6a83d1e253")
data = response.json()

imgs = ['cactus.jpg', 'clock.jpg', 'bread.jpg']


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<int:post_id>')
def post(post_id):
    global data
    global imgs
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
    app.run()
