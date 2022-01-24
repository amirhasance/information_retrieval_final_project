from typing import Tuple, List, Dict

from my_index.non_positional.DocTerm import TermPostingList
from adapter.adapter import Doc
from my_tokenizer.m_tokenizer import get_token_stream, KnnTokenizer
from utils.utils import Utils


class Index:
    def __init__(self):
        self.inverted_index: Dict[str:TermPostingList] = dict()  # dict { key = term , value = term_posting_list }
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


class KnnIndex(Index):
    def __init__(self):
        super().__init__()
        self.get_token_stream: List[Tuple[List, Doc]] = KnnTokenizer().get_tokenized_stream()

    def create_index(self):
        for tokens, doc in self.get_token_stream:
            for token in tokens:
                if token not in self.inverted_index.keys():
                    self.inverted_index[token] = TermPostingList(token)
                self.inverted_index[token].insert(doc_id=doc.doc_id)
        Utils.save_object_to_file(self.inverted_index, 'knn_inverted_index')


if __name__ == '__main__':
    a = KnnIndex()
    a.create_index()
    # a = {"name" :"amir"}
    Utils.save_object_to_file(a.inverted_index, 'knn_inverted_index')
    # a = Utils.load_object_from_file('knn_inverted_index')
    print(a)
