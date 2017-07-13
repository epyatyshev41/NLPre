#import pattern.en
import spacy
from tokenizers import meta_text
import logging

'''
_POS_shorthand = {
    "adjective": "ADJ",
    "noun": "N",
    "verb": "V",
    "modal_verb": "V",
    "adverb": "RB",
    "unknown": "UNK",
    "pronoun": "POS",
    "connector": "CC",
    "punctuation": "PUNC",
    "cardinal": "CD",
    "w_word": "WV",
    'quote': "QUOTE",
    "symbol": "SYM",
}
'''

class pos_tokenizer(object):

    """
    Removes all words that are of a designated part-of-speech (POS) from
    a document. For example, when processing medical text, it is useful to
    remove all words that are not nouns or adjectives. POS detection is
    provided by the spaCy.io. Parts of speech:

    POS = 
       "punctuation" : punctuation and symbols [PUNCT, SYM]
       "noun" : nouns and proper nouns
       "adjective": 
    "unknown": ["X"],
    "noun":

    "pronoun":

    }

    """

    def __init__(self, POS_blacklist):
        """
        Initialize the parser.

        Args:
            POS_blacklist: A list of parts of speech to remove from the text.
        """
        self.logger = logging.getLogger(__name__)
        self.nlp = spacy.load('en')

        POS = {
            "noun"         : ["NOUN",],
            "proper_noun"  : ["PROPN",],
            "adjective"    : ["ADJ"],
            "verb"         : ["VERB"],
            "adverb"       : ["ADV",],
            "punctuation"  : ["PUNCT","SYM", "NUM", "PART",],
            "connector"    : ["CCONJ", "CONJ", "DET", "ADP", "INTJ","PRON"],
            "unknown"      : ["X"],
        }

        self.filtered_POS = POS_blacklist
        self.POS_map = {}
        for pos, L in POS.items():
            for y in L:
                self.POS_map[y] = pos

    def __call__(self, text, force_lemma=True):
        '''
        Runs the parser.

        Args:
            text: a string document
            force_lemma: bool, lemmitze the words prior to parsing
        Returns:
            results: A string document
        '''

        # Due to spaCy.ios handling of hyphens, we need to mask them beforehand
        text = text.replace('-', '_HYPHENNN')
        print text
        
        proc_text = self.nlp(text)

        pos_tags = []
        doc2 = []
        removedWords = []
        
        for sent in self.nlp(text).sents:

            sent2 = []
            for token in sent:

                
                # Skip extra spaces
                if token.is_space:
                    continue
                
                if force_lemma:
                    num_caps = sum((x.isupper() for x in token.text))

                    # For words with multiple caps, don't lemmatize
                    if num_caps > 1:
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
                    pos = self.POS_map[token.pos_]

                if pos in self.filtered_POS:
                    removedWords.append(word)
                    continue

                sent2.append(word)
                pos_tags.append(pos)
                
                print token, pos, token.tag_

            
            doc2.append(' '.join(sent2))

        doc2 = '\n'.join(doc2)

        # Undo the spaCy.io hack
        doc2 = doc2.replace('_HYPHENNN', '-')
        
        self.logger.info('Removed words: %s' % removedWords)

        # The number of POS tokens should match the number of word tokens
        assert(len(pos_tags) == len(doc2.split()))

        result = meta_text(doc2, POS=pos_tags)
        return result

        '''
        exit()

        pos_tags = []
        tokens = self.parse(text)
        doc2 = []
        removedWords = []

        for sentence in tokens.split():
            sent2 = []

            for word, tag in sentence:

                if "PHRASE_" in word:
                    sent2.append(word)
                    pos_tags.append(_POS_shorthand["noun"])
                    continue

                if "MeSH_" in word:
                    sent2.append(word)
                    pos_tags.append(_POS_shorthand["noun"])
                    continue

                tag = tag.split('|')[0].split('-')[0].split("&")[0]

                # try:
                #    pos = self.POS_map[tag]
                # except BaseException:
                #    self.logger.info("UNKNOWN POS *{}*".format(tag))
                #    pos = "unknown"

                pos = self.POS_map[tag]

                if pos in self.filtered_POS:
                    removedWords.append(word)
                    continue

                word = pattern.en.singularize(word, pos)

                if pos == "verb" or force_lemma:
                    lem = pattern.en.lemma(word, parse=False)
                    if lem is not None:
                        word = lem

                sent2.append(word)
                pos_tags.append(_POS_shorthand[pos])

            doc2.append(' '.join(sent2))

        doc2 = '\n'.join(doc2)

        self.logger.info('Removed words: %s' % removedWords)

        # The number of POS tokens should match the number of word tokens
        assert(len(pos_tags) == len(doc2.split()))

        result = meta_text(doc2, POS=pos_tags)
        return result
        '''
