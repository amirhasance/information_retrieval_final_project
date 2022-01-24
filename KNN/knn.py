import math
from threading import Thread
from typing import Tuple, List, Dict
from adapter.adapter import Doc, KnnAdapter
from my_tokenizer.m_tokenizer import KnnTokenizer, MyTokenizer
from utils.utils import Utils
from vertex.doc_vertex import Vertex
from typing import Set
import numpy as np
import pandas as pd


class DocumentsVertex:

    def __init__(self):
        self.inverted_index = Utils.load_object_from_file('knn_inverted_index')
        self.N = 50_000
        self.doc_vertex = dict()
        # self.term_idf_dict = dict()
        # self.doc_id_to_category = dict()
        # self.term_to_termid = dict()
        self.doc_vertex = Utils.load_object_from_file('knn3_doc_vertex')
        self.term_idf_dict: Dict = Utils.load_object_from_file('knn_term_idf_dict')  # { term : idf log(N/nt) }
        self.doc_id_to_category: Dict = Utils.load_object_from_file('knn_docid_to_category')
        self.term_to_termid: Dict = Utils.load_object_from_file('knn_term_to_termid')
        self.get_token_stream: List[Tuple[List, Doc]] = KnnTokenizer().get_tokenized_stream()

    def loop(self):
        for tokens, doc in self.get_token_stream:
            print(doc.doc_id)
            thread = Thread(target=self.create_weighted_vertex, args=(tokens, doc))
            thread.start()
        # Utils.save_object_to_file(a.doc_id_to_category, 'knn3_docid_to_category')
        Utils.save_object_to_file(a.doc_vertex, 'knn3_doc_vertex')
        # Utils.save_object_to_file(a.term_to_termid, 'knn3_term_to_termid')
        # Utils.save_object_to_file(a.term_idf_dict, 'knn3_term_idf_dict')

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
        if term_idf > 2.2:
            df_t = self.inverted_index.get(term).posting_list.get(doc_id).doc_frequency
            w = (1 + math.log10(df_t)) * (term_idf)
            if df_t:
                return w
            return 0

    def create_vertex_for_unlabled_doc(self, tokens):
        terms = set(tokens)
        tf_dict = dict()
        for term in terms:
            idf = self.term_idf_dict.get(term)
            if idf and idf > 2.2:
                if tf_dict.get(term):
                    tf_dict[term] += 1
                else:
                    tf_dict[term] = 1
        vertex = Vertex(doc_id=None)
        for term in tf_dict.keys():
            term_id = self.term_to_termid.get(term)
            if term_id:
                term_idf = self.term_idf_dict.get(term)
                if term_idf is None:
                    tf = self.inverted_index.get(term).posting_list.__len__()
                    term_idf = math.log10(self.N / tf)
                    self.term_idf_dict[term] = term_idf
                w = (1 + math.log10(tf_dict.get(term))) * (term_idf)
                vertex.term_weight_dict[term_id] = w
        vertex.terms = list(tf_dict.keys())
        return vertex

    def get_candid_documents_from_invertd_index(self, terms: Set[str]) -> List[Vertex]:
        candid_doc: List[Vertex] = list()
        candid_doc_id_set = set()
        for term in terms:
            if self.inverted_index.get(term):
                term_posting_list = self.inverted_index.get(term).posting_list
                for posting in term_posting_list.values():
                    candid_doc_id_set.add(posting.docId)
        for candid_doc_id in candid_doc_id_set:
            candid_doc.append(self.doc_vertex.get(candid_doc_id))

        return candid_doc

    @staticmethod
    def calculate_cosin_similarity(doc1: Dict, doc2: Dict):

        intersection = set(doc1.keys()).intersection(doc2.keys())
        if len(intersection):
            vect1 = [doc1.get(key) for key in intersection]
            vec2 = [doc2.get(key) for key in intersection]
            norm_vect_1 = np.linalg.norm(list(doc1.values()))
            norm_vect_2 = np.linalg.norm(list(doc2.values()))
            inner_product = pd.Series(vect1).dot(pd.Series(vec2))
            cosin_similarity = inner_product / (norm_vect_1 * norm_vect_2)
            return cosin_similarity
        return 0

    def classify(self):
        unlabaled_docs = MyTokenizer().get_tokenized_stream()
        for doc_id, tokens, doc_title in unlabaled_docs:
            self.single_thread_classification(doc_id, tokens)

    def single_thread_classification(self, doc_id, tokens, ):
        vertex = self.create_vertex_for_unlabled_doc(tokens)
        terms: Set = set(vertex.terms)
        candid_doc_vertex_list: List[Vertex] = self.get_candid_documents_from_invertd_index(terms)
        ranked_documetns = dict()
        for doc_vertex in candid_doc_vertex_list:
            similarity = self.calculate_cosin_similarity(doc_vertex.term_weight_dict,
                                                         vertex.term_weight_dict)
            ranked_documetns[doc_vertex.doc_id] = similarity
        ranked_documetns = {k: v for k, v in
                            sorted(ranked_documetns.items(), key=lambda item: item[1], reverse=True)}
        k = 5
        top_k_doc_id_list = list(ranked_documetns.keys())[:k]
        knn_category = dict()
        for i in range(k):
            category = self.doc_id_to_category.get(top_k_doc_id_list[i])
            if knn_category.get(category):
                knn_category[category] += 1
            else:
                knn_category[category] = 1
        knn_category = {k: v for k, v in
                        sorted(knn_category.items(), key=lambda item: item[1], reverse=True)}
        print(doc_id, knn_category)


if __name__ == '__main__':
    a = DocumentsVertex()
    # a.loop()

    # a = DocumentsVertex().create_weighted_vertex()

    a.classify()
