from flask import Flask, render_template, request
from textalyzer.summarizer import TextSummarizer
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/summarizer', methods=['POST', 'GET'])
def summarizer():
    if request.method == "POST":
        original_text = request.form['originaltext']
        percentage = int(request.form['percslider'])

        summarize_obj = TextSummarizer()
        summarize_obj.preprocess_text(original_text)
        summary = summarize_obj.make_summary(percentage)

        return render_template(
            'summarizer.html', original_text=original_text,
            summarized_text=summary, slider_value=percentage)
    else:
        return render_template('summarizer.html')


@app.route('/about')
def about():
    return render_template('about.html')


def main():
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
