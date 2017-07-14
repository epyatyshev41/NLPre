# import pattern.en
import spacy
from tokenizers import meta_text
import logging


class pos_tokenizer(object):

    """
    Removes all words that are of a designated part-of-speech (POS) from
    a document. For example, when processing medical text, it is useful to
    remove all words that are not nouns or adjectives. POS detection is
    provided by the spaCy.io.

    See more here:
    https://spacy.io/docs/usage/pos-tagging

    """

    def __init__(self, blacklist):
        """
        Initialize the parser.

        Args:
            blacklist: A list of parts of speech to remove from the text.
        """
        self.logger = logging.getLogger(__name__)
        self.nlp = spacy.load('en')
        self.set_blacklist(blacklist)

    def set_blacklist(self, blacklist):

        self.POS_map = {
            "-LRB-": "punctuation",
            "-RRB-": "punctuation",
            ",": "punctuation",
            ":": "punctuation",
            ".": "punctuation",
            "''": "quote",
            "": "quote",
            "#": "symbol",
            "``": "quote",
            "$": "symbol",
            "ADD": "email",
            "AFX": "affix",
            "BES": "common_verb",
            "CC": "connector",
            "CD": "number",
            "DT": "determiner",
            "EX": "common_verb",
            "FW": "unknown",
            "GW": "unknown",
            "HVS": "common_verb",
            "HYPH": "symbol",
            "IN": "connector",
            "JJ": "adjective",
            "JJR": "adjective",
            "JJS": "adjective",
            "LS": "symbol",
            "MD": "common_verb",
            "NFP": "punctuation",
            "NIL": "unknown",
            "NN": "noun",
            "NNP": "noun",
            "NNPS": "noun",
            "NNS": "noun",
            "PDT": "common_verb",
            "POS": "possessive_ending",
            "PRP": "pronoun",
            "PRP$": "pronoun",
            "RB": "adverb",
            "RBR": "adverb",
            "RBS": "adverb",
            "RP": "adverb",
            "SP": "space",
            "SYM": "symbol",
            "TO": "common_verb",
            "UH": "connector",
            "VB": "verb",
            "VBD": "verb",
            "VBG": "verb",
            "VBN": "verb",
            "VBP": "verb",
            "VBZ": "verb",
            "WDT": "common_verb",
            "WP": "common_verb",
            "WP$": "common_verb",
            "WRB": "common_verb",
            "XX": "unknown",
        }

        self.blacklist = blacklist

        return self

    def __call__(self, text, lemmatize=True):
        '''
        Runs the parser.

        Args:
            text: a string document
            lemmatize: bool, lemmatize the words prior to parsing
        Returns:
            results: A string document
        '''

        # Due to spaCy.ios handling of hyphens, we need to mask them beforehand
        text = text.replace('-', '_HYPHENNN')

        pos_tags = []
        doc2 = []
        removedWords = []

        for sent in self.nlp(text).sents:

            sent2 = []
            for token in sent:

                # Skip extra spaces
                if token.is_space:
                    continue

                # There are so many different pronouns in spaCy, if we find one
                # and we don't want it, remove it here
                if token.lemma_ == "-PRON-" and "pronoun" in self.blacklist:
                    removedWords.append(token.text)
                    continue

                if lemmatize:
                    num_caps = sum((x.isupper() for x in token.text))

                    # For words with multiple caps, don't lemmatize
                    if num_caps > 1:
                        word = token.text
                    # Don't use spaCy's fancy PRON
                    elif token.lemma_ == "-PRON-":
                        word = token.text
                    # For words that start with a cap, only correct this
                    elif token.text[0].isupper():
                        word = token.text[0] + token.lemma_[1:]
                    # Otherwise lemmatize
                    else:
                        word = token.lemma_

                else:
                    word = token.text

                # Words with underscores are marked as nouns
                if "_" in word:
                    pos = "noun"
                else:
                    pos = self.POS_map[token.tag_]

                if pos in self.blacklist:
                    removedWords.append(word)
                    continue

                sent2.append(word)
                pos_tags.append(pos)

            doc2.append(' '.join(sent2))

        doc2 = '\n'.join(doc2)

        # Undo the spaCy.io hack
        doc2 = doc2.replace('_HYPHENNN', '-')

        self.logger.info('Removed words: %s' % removedWords)

        # The number of POS tokens should match the number of word tokens
        assert(len(pos_tags) == len(doc2.split()))

        result = meta_text(doc2, POS=pos_tags)
        return result
