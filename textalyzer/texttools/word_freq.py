from textalyzer.texttools import TextTool
from wordcloud import WordCloud
import numpy as np
from typing import List


class WordFreq(TextTool):
    def __init__(self, language: str = 'en'):
        """Word frequency
        Preprocesses the text and then uses spacy filters to determine
        the term frequency and plot the result.

        Parameters
        ----------
        language: str (default: "en")
            Which languagemodel to use, only English ("en")
            and Dutch ("nl") are supported at the moment
        """
        super().__init__(language)

    def plot_wordfreq(self, max_terms: int = 10) -> List:
        """Plot keyword frequency

        Parameters
        ----------
        max_terms: int (default: 10)
            The maximum number of terms to plot

        Returns
        -------
        A list of dictionaries with the wordfreq (visualisation is done through d3)
        """
        word_array = np.array(list(self.freq_word.keys()))
        value_array = np.array(list(self.freq_word.values()))

        top_indices = np.argsort(-value_array)[:max_terms]
        top_words = word_array[top_indices]
        top_values = value_array[top_indices]

        return [{'term': word, 'freq': freq} for word, freq in zip(top_words, top_values)]

    def plot_wordcloud(self, max_terms: int = 10) -> str:
        """Plot wordcloud

        Parameters
        ----------
        max_terms: int (default: 10)
            The maximum number of terms to plot

        Returns
        -------
        A wordcloud with the max frequency terms
        """
        wc = WordCloud(background_color='white', max_words=max_terms,
                       width=800, height=600)

        # generate word cloud
        wc.generate_from_frequencies(self.freq_word)
        return wc.to_array()
