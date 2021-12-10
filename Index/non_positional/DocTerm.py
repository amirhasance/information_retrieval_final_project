from typing import Dict


class Posting:
    def __init__(self, doc_id):
        self.doc_frequency = 0
        self.docId = doc_id

    def insert(self):
        self.doc_frequency += 1


class TermPostingList:
    def __init__(self, term: str):
        self.term_frequency = 0
        self.posting_list: Dict[Posting] = dict()  # dictionary { key = doc_id : value = Posting(doc_id , repeat)}
        self.term = term

    def insert(self, doc_id):
        self.term_frequency += 1
        if doc_id not in self.posting_list.keys():
            self.posting_list[doc_id] = Posting(doc_id)
        self.posting_list[doc_id].insert()
