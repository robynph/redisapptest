# in app.py
import os
from flask import Flask, jsonify, url_for, request, redirect

from rq import Queue
from rq.job import Job
from worker import conn
from utils import count_words_at_url

app = Flask(__name__)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

def count_and_save_words(url):

    errors = []

    try:
        r = requests.get(url)
    except:
        errors.append(
            "Unable to get URL. Please make sure it's valid and try again."
        )
        return {"error": errors}

    # text processing
    raw = BeautifulSoup(r.text).get_text()
    nltk.data.path.append('./nltk_data/')  # set the path
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)

    # remove punctuation, count raw words
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)

    # stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)

    # save the results
    try:
        result = Result(
            url=url,
            result_all=raw_word_count,
            result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
        return result.id
    except:
        errors.append("Unable to add item to database.")
        return {"error": errors}

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == "POST":
        # this import solves a rq bug which currently exists
        from app import count_and_save_words

        # get url that the person has entered
        url = request.form['url']
        if not url[:8].startswith(('https://', 'http://')):
            url = 'http://' + url
        job = q.enqueue_call(
            func=count_and_save_words, args=(url,), result_ttl=5000
        )
        print(job.get_id())

    return render_template('index.html', results=results)

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
