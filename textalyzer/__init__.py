from flask import Flask, render_template, request, abort
from textalyzer.texttools import TextSummarizer, WordFreq
from base64 import b64encode
from io import BytesIO
from PIL import Image

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
        text_language = form['language']

        summarize_obj = TextSummarizer(text_language)
        summarize_obj.preprocess_text(original_text)
        summary, input_length = \
            summarize_obj.make_summary(sent_length)
    except Exception as e:
        abort(400, e)
    return {'summary': summary, 'input_length': input_length}


@app.route('/wordfreqs')
def wordfreqs():
    return render_template('wordfreq.html')


@app.route('/make_wordfreq', methods=['POST'])
def make_wordfreq():
    try:
        form = request.json
        original_text = form['originaltext']
        max_words = int(form['maxterms'])
        wordcloud = form['wordcloud']
        text_language = form['language']

        wordfreq_obj = WordFreq(text_language)
        wordfreq_obj.preprocess_text(original_text)

        buf = BytesIO()
        if wordcloud == 'wordcloud':
            wordfreq_plot = \
                wordfreq_obj.plot_wordcloud(max_words)
            pil_img = Image.fromarray(wordfreq_plot)
            pil_img.save(buf, format='png')
        else:
            wordfreq_plot = \
                wordfreq_obj.plot_wordfreq(max_words)
            wordfreq_plot.savefig(buf, format='png')

        embedded_plot = b64encode(buf.getbuffer()).decode("ascii")
    except Exception as e:
        abort(400, e)

    return {'image': embedded_plot}


@app.route('/about')
def about():
    return render_template('about.html')


def main():
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()
