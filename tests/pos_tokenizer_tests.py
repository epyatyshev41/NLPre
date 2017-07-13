from nose.tools import *
from nlpre import pos_tokenizer

base_blacklist = [
    "connector",
    "pronoun",
    "adverb",
    "symbol",
    "verb",
    "punctuation",
]

class POS_Tokenizer_Test:

    @classmethod
    def setup_class(cls):
        cls.parser = pos_tokenizer([])

    def keep_nouns_test1(self):
        doc = u"The boy threw the ball into the yard"
        doc_right = u"boy ball yard"
        doc_new = self.parser.set_blacklist(base_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test2(self):
        doc = u"So we beat on, boats against the current, borne back ceaselessly into the past"
        doc_right = u"boat current past"
        doc_new = self.parser.set_blacklist(base_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test3(self):
        doc = u" A screaming comes across the sky. It has happened before, but there is nothing to compare it to now."
        doc_right = u"screaming sky\nnothing"
        doc_new = self.parser.set_blacklist(base_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test4(self):
        doc = (u"Many years later, as he faced the firing squad, he was to remember that distant"
               u" afternoon when his father took him to discover ice")
        doc_right = u"Many year fire squad distant afternoon father ice"
        doc_new = self.parser.set_blacklist(base_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test5(self):
        doc = u"The sky above the port was the color of television, tuned to a dead channel"
        doc_right = u"sky port color television dead channel"
        doc_new = self.parser.set_blacklist(base_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test6(self):
        doc = (u"In my younger and more vulnerable years my father gave me some advice that "
               u"I've been turning over in my mind ever since")
        doc_right = u"younger vulnerable year father advice mind"
        doc_new = self.parser.set_blacklist(base_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_mesh_test(self):
        doc = u"The boy MeSH_Threw the ball into the yard"
        doc_right = u"boy MeSH_Threw ball yard"
        doc_new = self.parser.set_blacklist(base_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_phrase_test(self):
        doc = u"The boy PHRASE_Threw the ball into the yard"
        doc_right = u"boy PHRASE_Threw ball yard"
        doc_new = self.parser.set_blacklist(base_blacklist)(doc)

        assert_equal(doc_right, doc_new.text)

    def possesive_word_test(self):
        doc = u"I am Jack's complete lack of surprise"
        doc_right = u"be jack complete lack of surprise"
        doc_new = self.parser.set_blacklist(["pronoun"])(doc)

        assert_equal(doc_right, doc_new.text)

    def cardinal_word_test(self):
        doc = u"There are two phases."
        doc_right = u"There be phase ."
        doc_new = self.parser.set_blacklist(["punctuation"])(doc)
        
        assert_equal(doc_right, doc_new.text)

    def w_word_test(self):
        doc = u"Transcriptions that are observed."
        doc_right = u"Transcription be observe ."
        doc_new = self.parser.set_blacklist(["w_word"])(doc)
        
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

    # def unknown_word_test(self):
    #    doc = 'The boy akjf45!naf the ball into the yard'
    #    doc_right = 'boy akjfnaf ball yard'
    #    doc_new = self.parser(doc)
    #    assert_equal(doc_right, doc_new.text)
