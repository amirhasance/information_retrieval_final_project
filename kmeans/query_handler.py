import math
from typing import List, Dict
from hazm import Normalizer
from parsivar import Tokenizer
from adapter.adapter import N
from kmeans.cluster import KmeanCluster
from my_tokenizer.m_tokenizer import MyTokenizer
from utils.utils import Utils
from vertex.doc_vertex import Vertex
from cluster import Cluster

inverted_index = Utils.load_object_from_file('non_pos_inverted_index')
kmeans_cluster = Utils.load_object_from_file('KmeansCluster_objects_after_4times_reassign')
doc_id_to_doc_title = Utils.load_object_from_file("doc_id_to_doc_title")


class QueryHandler:
    def __init__(self, inverted_index: dict, b: int = 2, doc_id_to_doc_title: Dict = None):
        self.inverted_index = inverted_index
        self.N = N
        self.term_idf_dict = dict()
        self.kmeans_cluster: KmeanCluster = kmeans_cluster
        self.b = b
        if doc_id_to_doc_title is None:
            self.doc_id_to_doc_title = dict()

    def create_query_vector(self, query: str):
        normalized_query: str = Normalizer().normalize(query)
        token_words: List = Tokenizer().tokenize_words(normalized_query)
        token_words = list(filter(lambda x: x not in MyTokenizer.get_stop_words(), token_words))
        query_index = dict()
        for token in token_words:
            if query_index.get(token):
                query_index[token] += 1
            else:
                query_index[token] = 1
        v = Vertex()  # simply considered query as a document with doc_id = -1
        for term, term_freq in query_index.items():
            term_idf = self.term_idf_dict.get(term)
            if term_idf is None:
                tn = self.inverted_index.get(term).posting_list.__len__()
                term_idf = math.log10(self.N / tn)
                self.term_idf_dict[term] = term_idf
            term_id = list(self.inverted_index.keys()).index(term)
            weight = (1 + math.log10(term_freq)) * term_idf
            v.term_weight_dict[term_id] = weight
        return v

    def handle_query(self, query):
        query_vector = self.create_query_vector(query).term_weight_dict
        centroid_similarity = dict()
        for index, cluster in enumerate(self.kmeans_cluster.clusters):
            centroid = cluster.centroid
            similarity = self.kmeans_cluster.calculate_cosin_similarity(centroid, query_vector)
            centroid_similarity[index] = similarity
        centroid_similarity = {k: v for k, v in
                               sorted(centroid_similarity.items(), key=lambda item: item[1], reverse=True)}
        final_answer = dict()  # doc_id : score
        for i in range(self.b):
            centroid_index = list(centroid_similarity)[i]
            cluster = self.kmeans_cluster.clusters[centroid_index]
            for doc_vertex in cluster.members:
                similarity = KmeanCluster.calculate_cosin_similarity(doc_vertex.term_weight_dict, query_vector)
                final_answer[doc_vertex.doc_id] = similarity
        final_answer = {k: v for k, v in sorted(final_answer.items(), key=lambda item: item[1], reverse=True)}
        return final_answer


if __name__ == '__main__':
    handler = QueryHandler(inverted_index=inverted_index, doc_id_to_doc_title=doc_id_to_doc_title)
    handler.handle_query("دانشگاه صنعتی امیرکبیر")
