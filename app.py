import os
from flask import Flask, request
from flask_cors import CORS
from indexgenerator import generator
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='getyourindex@gmail.com',
    MAIL_PASSWORD='Indexer2020*'
)

mail = Mail(app)

@app.route('/<email>', methods=["POST"])
def send_index(email):
    ms = request.files['ms']
    words = request.files['words']

    message = 'here is your index'
    subject = "your index"
    generator(ms, words)

    msg = Message(recipients=[email],
                  sender="getyourindex@gmail.com",
                  body=message,
                  subject=subject)

    with app.open_resource("index.txt") as fp:
        msg.attach("index.txt", "text/plain", fp.read())

    mail.send(msg)
    os.remove("index.txt")

    return {'result': "Hello World"}


