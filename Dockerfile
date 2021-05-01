FROM python:3.8-slim

LABEL author="Ruben Peters"

WORKDIR /app

COPY . .

# Install the Python package
RUN pip install -e .

# Download language models
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download nl_core_news_sm

EXPOSE 8000

CMD gunicorn textalyzer.__init__:app -w 2 --threads 2 -b 0.0.0.0:8000