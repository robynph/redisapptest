# in app.py
import os
from flask import Flask, jsonify, url_for, request, redirect

from rq import Queue
from worker import conn
from utils import count_words_at_url

app = Flask(__name__)
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

@app.route("/count", methods=["POST"])
def count():
    print('task in app.py')
    q = Queue(connection=conn)
    result = q.enqueue(count_words_at_url, 'https://heroku.com')
    return jsonify({"result": result})
