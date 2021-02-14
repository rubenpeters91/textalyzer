from flask import Flask, render_template, request, abort
from textalyzer.summarizer import TextSummarizer
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/summarizer')
def summarizer():
    return render_template('summarizer.html')


@app.route('/make_summary', methods=['POST'])
def make_summary():
    try:
        form = request.json
        original_text = form['originaltext']
        sent_length = int(form['sentlength'])

        summarize_obj = TextSummarizer()
        summarize_obj.preprocess_text(original_text)
        summary, input_length = \
            summarize_obj.make_summary(sent_length)
    except Exception as e:
        abort(400, e)
    return {'summary': summary, 'input_length': input_length}


@app.route('/about')
def about():
    return render_template('about.html')


def main():
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
