import spacy


class TextSummarizer():
    def __init__(self, language="en"):
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

    def _calc_word_dict(self, all_words):
        """Calculate the term frequencies

        Uses a dictionary to store the word frequencies
        And divides by max frequency to normalise

        Parameters
        ----------
        all_words: list of str
            A list of all the words in the document

        Returns
        -------
        freq_word: dict
            A dictionary with for every unique word,
            its normalized frequency
        """
        freq_word = {}

        for word in all_words:
            word_lower = word.lower()
            if word_lower in freq_word.keys():
                freq_word[word_lower] += 1
            else:
                freq_word[word_lower] = 1

        max_freq = max(freq_word.values())
        for word in freq_word.keys():
            freq_word[word] = freq_word[word] / max_freq

        return freq_word

    def _calc_sent_strength(self, sentences):
        """Calculate the sentence strength

        Using the word frequencies, determine
        the score for every sentence

        Parameters
        ----------
        sentences: list of Spacy tokens
            The ouput from doc.sent

        Returns
        -------
        sent_strength: dict
            Dictionary that contains the strength per sentence
        """
        sent_strength = {}
        for sent in sentences:
            for word in sent:
                word_index = word.text.lower()
                if word_index in self.freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent] += self.freq_word[word_index]
                    else:
                        sent_strength[sent] = self.freq_word[word_index]
        return sent_strength

    def preprocess_text(self, text):
        """Preprocess input text

        Preprocesses the text by filtering with Spacy and
        then calculating term frequencies and sentence strengths

        Parameters
        ----------
        text: str
            The complete unprocessed input data
        """
        doc = self.nlp(text)
        pos_tags = ['PROPN', 'ADJ', 'NOUN', 'VERB']
        all_words = [word.text for word in doc if word.pos_ in pos_tags]

        self.freq_word = self._calc_word_dict(all_words)
        self.sent_strength = self._calc_sent_strength(doc.sents)

    def make_summary(self, perc=30):
        """Make summary of the text

        Create a summary of the text by taking the
        top percentage sentences based on the calculated
        sentence_strength

        Parameters
        ----------
        perc: int
            Percentage of output sentences to return

        Returns
        -------
        The summary of the text as string

        """
        top_sentences = sorted(self.sent_strength.values())[::-1]
        top_index = int(perc/100 * len(top_sentences))
        top_sent = top_sentences[:top_index]

        summary = []
        for sent, strength in self.sent_strength.items():
            if strength in top_sent:
                summary.append(sent.text)
        return " ".join(summary)
