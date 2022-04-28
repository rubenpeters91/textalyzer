from textalyzer.texttools import TextTool
from wordcloud import WordCloud


class WordFreq(TextTool):
    def __init__(self, language: str = "en") -> None:
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

    def plot_wordfreq(self, max_terms: int = 10) -> list[dict]:
        """Plot keyword frequency

        Parameters
        ----------
        max_terms: int (default: 10)
            The maximum number of terms to plot

        Returns
        -------
        A list of dictionaries with the wordfreq
        (visualisation is done through d3)
        """
        top_words = self.freq_word.most_common(max_terms)

        return [{"term": word, "freq": freq} for word, freq in top_words]

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
        wc = WordCloud(
            background_color="white", max_words=max_terms, width=800, height=600
        )

        # generate word cloud
        wc.generate_from_frequencies(self.freq_word)
        return wc.to_array()
