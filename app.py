# in app.py

from flask import Flask, jsonify, url_for, request, redirect

from rq import Queue
from worker import conn
from utils import count_words_at_url

app = Flask(__name__)


@app.route("/count/< URL >", methods=["POST"])
def count(URL) -> str:
    print('task in app.py')
    q = Queue(connection=conn)
    result = q.enqueue(count_words_at_url, {URL})
    return jsonify("result": result)

if __name__ == "__main__":
    app.run(debug=True)
