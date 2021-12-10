from Index.non_positional.DocTerm import TermPostingList
from my_tokenizer.m_tokenizer import get_token_stream
from utils.utils import Utils


class Index:
    def __init__(self):
        self.inverted_index = dict()  # dict { key = term , value = term_posting_list }
        self.docid_to_doc_title = dict()  # dict { key = doc_id , value = doc_title}

    def create_index(self):
        for doc_id, terms, doc_title in get_token_stream:
            for term in terms:
                if term not in self.inverted_index.keys():
                    self.inverted_index[term] = TermPostingList(term)
                self.inverted_index[term].insert(doc_id=doc_id)
            self.docid_to_doc_title[doc_id] = doc_title

    def save_index_to_file(self):
        Utils.save_object_to_file(self.inverted_index, "non_pos_inverted_index")

