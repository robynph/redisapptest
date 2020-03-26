# in app.py

from flask import Flask, jsonify, url_for, request, redirect

from rq import Queue
from worker import conn
from utils import count_words_at_url

app = Flask(__name__)


@app.route("/count", methods=["POST"])
def count():
    print('task in app.py')
    q = Queue(connection=conn)
    result = q.enqueue(count_words_at_url, 'https://heroku.com')
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
