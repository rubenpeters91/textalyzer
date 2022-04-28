from typing import Iterator, Tuple

import numpy as np
from spacy.tokens import Span
from textalyzer.texttools import TextTool


class TextSummarizer(TextTool):
    def __init__(self, language: str = "en") -> None:
        """Text summarizer
        Preprocesses the text and then uses spacy filters to determine
        the most important sentences, based on term frequency in those
        sentences.

        Parameters
        ----------
        language: str (default: "en")
            Which languagemodel to use, only English ("en")
            and Dutch ("nl") are supported at the moment
        """
        super().__init__(language)

    def _calc_sent_strength(self, sentences: Iterator[Span]) -> None:
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

    def preprocess_text(self, text: str, lower_terms: bool = True) -> None:
        """Preprocess input text

        Preprocesses the text by filtering with Spacy and
        then calculating term frequencies and sentence strengths

        Parameters
        ----------
        text: str
            The complete unprocessed input data
        """
        super().preprocess_text(text, lower_terms=lower_terms)
        self._calc_sent_strength(self.doc.sents)

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
        if sent_length <= 1 or sent_length >= self.input_length:
            raise ValueError(
                "The output length has to be bigger than 1"
                " and can't be bigger than the input length"
            )

        sorted_indices = np.argsort(-self.sent_strength)
        top_indices = np.sort(sorted_indices[:sent_length])

        summary = self.sent_content[top_indices]
        summary_string = " ".join(summary)

        return summary_string, self.input_length
