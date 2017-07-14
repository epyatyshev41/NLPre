from nose.tools import *
from nlpre import pos_tokenizer

noun_blacklist = [
    "connector",
    "pronoun",
    "symbol",
    "punctuation",
    "determiner",
    "possessive_ending",
    "common_verb",
    "verb",
    "adverb",
    "number",
]

class POS_Tokenizer_Test:

    @classmethod
    def setup_class(cls):
        cls.parser = pos_tokenizer([])

    def keep_nouns_test1(self):
        doc = u"The boy threw the ball into the yard"
        doc_right = u"boy ball yard"
        doc_new = self.parser.set_blacklist(noun_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test2(self):
        doc = u"So we beat on, boats against the current, borne back ceaselessly into the past"
        doc_right = u"boat current past"
        doc_new = self.parser.set_blacklist(noun_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test3(self):
        doc = u" A screaming comes across the sky. It has happened before, but there is nothing to compare it to now."
        doc_right = u"screaming sky\nnothing"
        doc_new = self.parser.set_blacklist(noun_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test4(self):
        doc = (u"Many years later, as he faced the firing squad, he was to remember that distant"
               u" afternoon when his father took him to discover ice")
        doc_right = u"Many year firing squad distant afternoon father ice"
        doc_new = self.parser.set_blacklist(noun_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test5(self):
        doc = u"The sky above the port was the color of television, tuned to a dead channel"
        doc_right = u"sky port color television dead channel"
        doc_new = self.parser.set_blacklist(noun_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test6(self):
        doc = (u"In my younger and more vulnerable years my father gave me some advice that "
               u"I've been turning over in my mind ever since")
        doc_right = u"young vulnerable year father advice mind"
        doc_new = self.parser.set_blacklist(noun_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_mesh_test(self):
        doc = u"The boy MeSH_Threw the ball into the yard"
        doc_right = u"boy MeSH_Threw ball yard"
        doc_new = self.parser.set_blacklist(noun_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_phrase_test(self):
        doc = u"The boy PHRASE_Threw the ball into the yard"
        doc_right = u"boy PHRASE_Threw ball yard"
        doc_new = self.parser.set_blacklist(noun_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def possesive_word_test(self):
        doc = u"I am Jack's complete lack of surprise"
        doc_right = u"I be Jack complete lack of surprise"
        doc_new = self.parser.set_blacklist(["possessive_ending"])(doc)

        assert_equal(doc_right, doc_new.text)

    def common_verb_test(self):
        doc = u"Transcriptions that are observed."
        doc_right = u"Transcription be observe ."
        doc_new = self.parser.set_blacklist(["common_verb"])(doc)
        
        assert_equal(doc_right, doc_new.text)

    def quoted_word_test(self):
        doc = u'''We find the answer is "not quite".'''
        doc_right = u"We find the answer be not quite ."
        doc_new = self.parser.set_blacklist(["quote"])(doc)

        assert_equal(doc_right, doc_new.text)

    def symbol_test(self):
        doc = u'''I am #1.'''
        doc_right = u"I be 1 ."
        doc_new = self.parser.set_blacklist(["symbol"])(doc)

        assert_equal(doc_right, doc_new.text)
        
    def number_test(self):
        doc = u'''We are number one and twenty one.'''
        doc_right = u"We be number and ."
        doc_new = self.parser.set_blacklist(["number"])(doc)

        assert_equal(doc_right, doc_new.text)

    def lemmatize_test(self):
        doc = u'''I am a superstar.'''

        doc_right = u"I be a superstar ."
        doc_new = self.parser.set_blacklist([])(doc, lemmatize=True)
        assert_equal(doc_right, doc_new.text)

        doc_right = u"I am a superstar ."
        doc_new = self.parser.set_blacklist([])(doc, lemmatize=False)
        assert_equal(doc_right, doc_new.text)

        

