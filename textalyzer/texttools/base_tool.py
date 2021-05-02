import spacy
from typing import List


class TextTool():
    def __init__(self, language: str = "en"):
        """Text Tool
        Contains base functions and initializes an nlp object

        Parameters
        ----------
        language: str (default: "en")
            Which languagemodel to use, only English ("en")
            and Dutch ("nl") are supported at the moment
        """
        if language == 'en':
            self.nlp = spacy.load('en_core_web_sm')
        elif language == 'nl':
            self.nlp = spacy.load('nl_core_news_sm')
        else:
            NotImplementedError()

        self.pos_tags = ['PROPN', 'ADJ', 'NOUN', 'VERB']

    def _calc_word_dict(self, all_words: List[str]):
        """Calculate the term frequencies

        Uses a dictionary to store the word frequencies
        And divides by max frequency to normalise

        Parameters
        ----------
        all_words: list of str
            A list of all the words in the document
        """
        freq_word = {}

        for word in all_words:
            if word in freq_word.keys():
                freq_word[word] += 1
            else:
                freq_word[word] = 1

        max_freq = max(freq_word.values())
        freq_word = {
            key: value / max_freq for (key, value) in freq_word.items()}
        self.freq_word = freq_word

    def preprocess_text(self, text: str):
        """Preprocess input text

        Preprocesses the text by filtering with Spacy and
        then calculating term frequencies

        Parameters
        ----------
        text: str
            The complete unprocessed input data
        """
        self.doc = self.nlp(text)
        all_words = [
            word.lemma_.lower() for word in self.doc
            if word.pos_ in self.pos_tags]
        self._calc_word_dict(all_words)
