# in app.py
import os
from flask import Flask, jsonify, url_for, request, redirect

from rq import Queue
from rq.job import Job
from worker import conn
# from utils import count_words_at_url
#
q = Queue(connection=conn)

app = Flask(__name__)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == "POST":
        # this import solves a rq bug which currently exists
        from utils import count_words_at_url

        # get url that the person has entered
        url = "https://www.heroku.com"
        job = q.enqueue_call(
            func=count_words_at_url, args=(url), result_ttl=5000
        )
        print(job.get_id())

    return jsonify({"results":results, "job":job.get_id()})

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return "Nay!", 202
