from nlpre import identify_parenthetical_phrases
import collections


class corpus_acronym_counter(object):
    def __init__(self, documents):
        self.running_counter = collections.Counter()
        self.documents = documents
        self.counter = identify_parenthetical_phrases()

        for document in documents:
            count = self.counter(document)
            self.running_counter = self.running_counter + count

    def return_counter(self):
        return self.running_counter