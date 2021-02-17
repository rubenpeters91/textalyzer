from textalyzer.texttools import TextTool
from matplotlib.figure import Figure
import numpy as np


class WordFreq(TextTool):
    def __init__(self, language: str = 'en'):
        super().__init__(language)

    def plot_wordfreq(self, max_terms: int = 10):
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

        return fig
