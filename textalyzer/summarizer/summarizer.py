from typing import Tuple
import numpy as np
import spacy


class TextSummarizer():
    def __init__(self, language: str = "en"):
        """Text summarizer
        Preprocesses the text and then uses spacy filters to determine
        the most important sentences, based on term frequency in those
        sentences.

        Parameters
        ----------
        language: str (default: "en")
            Which languagemodel to use, only English supported at the
            moment
        """
        if language == "en":
            self.nlp = spacy.load("en_core_web_sm")
        else:
            NotImplementedError()

        self.pos_tags = ['PROPN', 'ADJ', 'NOUN', 'VERB']

    def _calc_word_dict(self, all_words: list[str]):
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

    def _calc_sent_strength(self, sentences: spacy.tokens.Span):
        """Calculate the sentence strength

        Using the word frequencies, determine
        the score for every sentence

        Parameters
        ----------
        sentences: list of Spacy tokens
            The ouput from doc.sent
        """
        sent_content = []
        sent_strength = []
        for sent_index, sent in enumerate(sentences):
            sent_content.append(sent.text)
            sent_strength.append(0)
            for word in sent:
                word_index = word.lemma_.lower()
                if word_index in self.freq_word.keys():
                    sent_strength[sent_index] += self.freq_word[word_index]

        self.sent_content = np.array(sent_content)
        self.sent_strength = np.array(sent_strength)
        self.input_length = len(self.sent_content)

    def preprocess_text(self, text: str):
        """Preprocess input text

        Preprocesses the text by filtering with Spacy and
        then calculating term frequencies and sentence strengths

        Parameters
        ----------
        text: str
            The complete unprocessed input data
        """
        doc = self.nlp(text)
        all_words = [
            word.lemma_.lower() for word in doc if word.pos_ in self.pos_tags]
        self._calc_word_dict(all_words)
        self._calc_sent_strength(doc.sents)

    def make_summary(self, sent_length: int = 5) -> Tuple[str, int]:
        """Make summary of the text

        Create a summary of the text by taking the
        top percentage sentences based on the calculated
        sentence_strength

        Parameters
        ----------
        sent_length: int
            Number of output sentences to return

        Returns
        -------
        summary_string: str
            The resulting summary string
        input_length: int
            The original length of the input
        """
        assert (sent_length >= 1) & (sent_length <= self.input_length),\
            'The output length has to be bigger than 1'\
            ' and can\'t be bigger than the input length'

        sorted_indices = np.argsort(-self.sent_strength)
        top_indices = np.sort(sorted_indices[:sent_length])

        summary = self.sent_content[top_indices]
        summary_string = ' '.join(summary)

        return summary_string, self.input_length
