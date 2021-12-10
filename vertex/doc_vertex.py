import math
from typing import Tuple, List, Dict
from hazm import Normalizer
from parsivar import Tokenizer
import collections

from adapter.adapter import N
from my_tokenizer.m_tokenizer import get_token_stream, MyTokenizer


class Vertex:
    def __init__(self, doc_id=None):
        self.doc_id = doc_id
        self.term_weight_dict = dict()  # dict{ key=term_id : value=weight }


class DocumentsVertex:

    def __init__(self, index: dict, doc_vertex: dict = None):
        self.inverted_index = index
        self.N = N
        self.doc_vertex = doc_vertex
        if self.doc_vertex is None:
            self.doc_vertex = dict()  # { key:doc_id , value: Vertex(doc_id)}
        self.term_idf_dict = dict()  # { term : idf log(N/nt) }
        self.term_to_termid = dict()

    def create_weighted_vertex(self):
        for doc_id, terms, _ in get_token_stream:
            document_vertex = Vertex(doc_id)
            for term in terms:
                term_id = self.term_to_termid.get(term)
                if term_id is None:
                    term_id = list(self.inverted_index.keys()).index(term)
                    self.term_to_termid[term] = term_id
                term_weight = self.calculate_term_weight_in_doc(term, doc_id)
                if term_weight:
                    document_vertex.term_weight_dict[term_id] = term_weight
            self.doc_vertex[doc_id] = document_vertex

    def calculate_term_weight_in_doc(self, term: str, doc_id):
        term_idf = self.term_idf_dict.get(term)
        if term_idf is None:
            tf = self.inverted_index.get(term).posting_list.__len__()
            term_idf = math.log10(self.N / tf)
            self.term_idf_dict[term] = term_idf
        df_t = self.inverted_index.get(term).posting_list.get(doc_id).doc_frequency
        w = (1 + math.log10(df_t)) * (term_idf)
        if df_t:
            return w
        return 0

    def get_ranked_result(self, query: str):
        query_vector, candid_documents = self.get_query_vector_and_candid_documents(query)
        ranked_result = dict()
        for doc_id in candid_documents:
            doc_vertex = self.doc_vertex.get(doc_id)
            rank = self.get_dot_product(query_vector, doc_vertex)
            if rank:
                ranked_result[doc_id] = rank
        return sorted(ranked_result.items(), key=lambda x: x[1], reverse=True)

    @staticmethod
    def get_dot_product(v1: Vertex, v2: Vertex):
        result = 0
        for term1_id in v1.term_weight_dict.keys():
            if term1_id in v2.term_weight_dict.keys():
                result += v1.term_weight_dict.get(term1_id) * v2.term_weight_dict.get(term1_id)
        v1_to_2 = 0
        for w in v1.term_weight_dict.values():
            v1_to_2 += w * w
        v2_to_2 = 0
        for w in v2.term_weight_dict.values():
            v2_to_2 += w * w
        return result / (math.sqrt(v2_to_2) * math.sqrt(v1_to_2))

    def get_query_vector_and_candid_documents(self, query):
        normalized_query: str = Normalizer().normalize(query)
        token_words: List = Tokenizer().tokenize_words(normalized_query)
        token_words = list(filter(lambda x: x not in MyTokenizer.get_stop_words(), token_words))
        query_index = dict()
        candid_documents = set()
        for token in token_words:
            if query_index.get(token):
                query_index[token] += 1
            else:
                query_index[token] = 1
        v = Vertex()  # simply considered query as a document with doc_id = -1
        for term, term_freq in query_index.items():
            for doc_id in self.inverted_index.get(term).posting_list.keys():
                candid_documents.add(doc_id)
            term_idf = self.term_idf_dict.get(term)
            if term_idf is None:
                tf = self.inverted_index.get(term).posting_list.__len__()
                term_idf = math.log10(self.N / tf)
                self.term_idf_dict[term] = term_idf
            term_id = list(self.inverted_index.keys()).index(term)
            weight = (1 + math.log10(term_freq)) * term_idf
            v.term_weight_dict[term_id] = weight
        return v, candid_documents
