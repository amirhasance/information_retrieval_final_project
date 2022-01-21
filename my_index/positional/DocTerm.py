from typing import Dict


class DocTerm:
    def __init__(self, doc_id, term_id):
        self.count = 0
        self.docId = doc_id
        self.termId = term_id
        self.positions = list()

    def insert(self, position):
        self.count += 1
        self.positions.append(position)
        self.positions = sorted(self.positions)


class Term:
    def __init__(self, id):
        self.count = 0
        self.id = id
        self.docTerms: Dict[DocTerm] = dict()

    def insert(self, doc_id, position):
        self.count += 1
        if doc_id not in self.docTerms.keys():
            self.docTerms[doc_id] = DocTerm(doc_id, self.id)
            sorted(self.docTerms.items())
        self.docTerms[doc_id].insert(position=position)
