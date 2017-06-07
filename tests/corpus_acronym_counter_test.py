from nlpre import corpus_acronym_counter
from nose.tools import assert_equal


class corpus_counter_test:
    def __init__(self):
        pass

    def corpus1_test(self):
        doc1 = 'The Office of the Director (OD) is the best'
        doc2 = "The Environmental Protection Agency (EPA) was created by Nixon"
        doc3 = ("The Environmental Protection Agency (EPA) was created by Nixon "
               "who loved the Environmental Protection Agency (EPA)")
        doc4 = 'A B C D E F G H I and Health and Human Services (HaHS) is important'
        doc5 = ("The Environmental Protection Agency (EPA) is not a government "
               "organization (GO) of Health and Human Services (HHS).")

        corpus = [doc1, doc2, doc3, doc4, doc5]

        corpus_counter = corpus_acronym_counter(corpus)
        corpus_count = corpus_counter.return_counter()


        counter_od = corpus_count[(('Office', 'of', 'the', 'Director'), 'OD')]
        counter_epa = corpus_count[
            (('Environmental', 'Protection', 'Agency'), 'EPA')]
        counter_hahs = corpus_count[(
            ('Health', 'and', 'Human', 'Services'), 'HaHS')]
        counter_hhs = corpus_count[(('Health', 'and', 'Human', 'Services'), 'HHS')]
        counter_go = corpus_count[(('government', 'organization'), 'GO')]

        assert_equal(counter_od, 1)
        assert_equal(counter_epa, 4)
        assert_equal(counter_hahs, 1)
        assert_equal(counter_hhs, 1)
        assert_equal(counter_go, 1)

