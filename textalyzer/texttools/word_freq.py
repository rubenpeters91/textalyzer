from textalyzer.texttools import TextTool
from matplotlib.figure import Figure
from wordcloud import WordCloud
import numpy as np


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

    def plot_wordfreq(self, max_terms: int = 10) -> Figure:
        """Plot keyword frequency

        Parameters
        ----------
        max_terms: int (default: 10)
            The maximum number of terms to plot

        Returns
        -------
        A Matplotlib Figure with the max frequency terms
        """
        word_array = np.array(list(self.freq_word.keys()))
        value_array = np.array(list(self.freq_word.values()))

        top_indices = np.argsort(-value_array)[:max_terms]
        top_words = word_array[top_indices]
        top_values = value_array[top_indices]
        y_pos = np.arange(len(top_words))

        fig = Figure()
        ax = fig.subplots()
        ax.barh(y_pos, top_values, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_words)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Frequency')
        ax.set_title(f'Top {max_terms} keywords in text')

        # removing the spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # removing the tick marks
        ax.tick_params(bottom="off", left="off")
        fig.tight_layout()
        return fig

    def plot_wordcloud(self, max_terms: int = 10) -> str:
        """Plot wordcloud

        Parameters
        ----------
        max_terms: int (default: 10)
            The maximum number of terms to plot

        Returns
        -------
        A Matplotlib Figure with the max frequency terms
        """
        wc = WordCloud(background_color='white', max_words=max_terms,
                       width=800, height=600)

        # generate word cloud
        wc.generate_from_frequencies(self.freq_word)
        return wc.to_array()
