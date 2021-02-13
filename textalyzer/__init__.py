from flask import Flask, render_template, request
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
    original_text = request.form['originaltext']
    percentage = int(request.form['percslider'])

    summarize_obj = TextSummarizer()
    summarize_obj.preprocess_text(original_text)
    summary = summarize_obj.make_summary(percentage)
    return summary


@app.route('/about')
def about():
    return render_template('about.html')


def main():
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
