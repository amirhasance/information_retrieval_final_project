import math
from threading import Thread
from typing import Tuple, List, Dict
from adapter.adapter import Doc, KnnAdapter
from my_tokenizer.m_tokenizer import KnnTokenizer, MyTokenizer
from utils.utils import Utils
from vertex.doc_vertex import Vertex


class DocumentsVertex:

    def __init__(self, doc_vertex: dict = None):
        self.inverted_index = Utils.load_object_from_file('knn_inverted_index')
        self.N = KnnAdapter().get_number_of_doc()
        self.doc_vertex = doc_vertex
        self.doc_vertex = Utils.load_object_from_file('knn_doc_vertex')
        self.term_idf_dict: Dict = Utils.load_object_from_file('knn_term_idf_dict')  # { term : idf log(N/nt) }
        self.doc_id_to_category: Dict = Utils.load_object_from_file('knn_doc_id_to_category')
        self.term_to_termid: Dict = Utils.load_object_from_file('knn_term_to_termid')
        self.get_token_stream: List[Tuple[List, Doc]] = KnnTokenizer().get_tokenized_stream()

    def loop(self):
        for tokens, doc in self.get_token_stream:
            thread = Thread(target=self.create_weighted_vertex, args=(tokens, doc))
            thread.start()

    def create_weighted_vertex(self, tokens, doc):
        document_vertex = Vertex(doc.doc_id)
        terms = set(tokens)
        for term in terms:
            term_id = self.term_to_termid.get(term)
            if term_id is None:
                term_id = list(self.inverted_index.keys()).index(term)
                self.term_to_termid[term] = term_id
            term_weight = self.calculate_term_weight_in_doc(term, doc.doc_id)
            if term_weight:
                document_vertex.term_weight_dict[term_id] = term_weight
        self.doc_vertex[doc.doc_id] = document_vertex
        self.doc_id_to_category[doc.doc_id] = doc.catergory

    def calculate_term_weight_in_doc(self, term: str, doc_id):
        term_idf = self.term_idf_dict.get(term)
        # term_idf = 1
        if term_idf is None:
            tf = self.inverted_index.get(term).posting_list.__len__()
            term_idf = math.log10(self.N / tf)
            self.term_idf_dict[term] = term_idf
        df_t = self.inverted_index.get(term).posting_list.get(doc_id).doc_frequency
        w = (1 + math.log10(df_t)) * (term_idf)
        if df_t:
            return w
        return 0

    def create_vertex_for_unlabled_doc(self, tokens):
        terms = set(tokens)
        vertex = Vertex()
        for term in terms:


    def classify(self):
        unlabaled_docs = MyTokenizer().get_tokenized_stream()
        for doc_id, tokens, doc_title in unlabaled_docs:
            print(doc_id, tokens, doc_title)


if __name__ == '__main__':
    a = DocumentsVertex()
    # a.loop()
    # a = DocumentsVertex().create_weighted_vertex()
    # Utils.save_object_to_file(a, 'knn_Document_vertex')
    # print(a)
    a.classify()
