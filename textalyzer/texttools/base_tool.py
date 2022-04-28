from collections import Counter

import spacy


class TextTool:
    def __init__(self, language: str = "en"):
        """Text Tool
        Contains base functions and initializes an nlp object

        Parameters
        ----------
        language: str (default: "en")
            Which languagemodel to use, only English ("en")
            and Dutch ("nl") are supported at the moment
        """
        if language == "en":
            self.nlp = spacy.load("en_core_web_sm")
        elif language == "nl":
            self.nlp = spacy.load("nl_core_news_sm")
        else:
            raise NotImplementedError()

        self.pos_tags = ["PROPN", "ADJ", "NOUN", "VERB"]

    def preprocess_text(self, text: str, lower_terms: bool = False):
        """Preprocess input text

        Preprocesses the text by filtering with Spacy and
        then calculating term frequencies

        Parameters
        ----------
        text: str
            The complete unprocessed input data
        lower_terms: bool
            Whether or not to lowercase all lemmas before counting them
        """
        self.doc = self.nlp(text)
        all_words = [word.lemma_ for word in self.doc if word.pos_ in self.pos_tags]

        if lower_terms:
            all_words = [word.lower() for word in all_words]
        self.freq_word = Counter(all_words)
