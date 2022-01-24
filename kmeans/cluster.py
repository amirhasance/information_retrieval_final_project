from typing import Dict, List
import pandas as pd
from utils.utils import Utils
import numpy as np
import random
from vertex.doc_vertex import Vertex


class KmeanCluster:

    def __init__(self, document_vertx=None, k: int = 15):
        if document_vertx is None:
            self.document_vertx: Dict[int, Vertex] = self.get_document_vertex()
        self.k: int = k
        self.clusters: List[Cluster] = list()
        self.create_first_cluster()

    def reassgin(self):
        self.cal_new_centroid_for_clusters()
        self.reassign_cluster_documetns()

    def cal_new_centroid_for_clusters(self):
        for cluster in self.clusters:
            new_centroid = dict()
            for cluster_member in cluster.members:
                member_vertex = cluster_member.term_weight_dict
                for key in member_vertex.keys():
                    if key in new_centroid.keys():
                        new_centroid[key] += member_vertex.get(key)
                    else:
                        new_centroid[key] = member_vertex.get(key)
            cluster_member_num = len(cluster.members)
            new_centroid_ = dict()
            for key, value in new_centroid.items():
                new_centroid_[key] = value / cluster_member_num
            cluster.centroid = new_centroid_

    def reassign_cluster_documetns(self):

        centroid_list = [cluster.centroid for cluster in self.clusters]
        new_clusters: List[Cluster] = list()
        for centroid in centroid_list:
            new_clusters.append(Cluster(centroid))
        for document_vertex in self.document_vertx.values():
            new_centroid = self.get_centorid_of_document(document_vertex.term_weight_dict)
            for cluster in new_clusters:
                if cluster.centroid == new_centroid:
                    cluster.members.append(document_vertex)
                    break

        self.clusters = new_clusters

    def create_first_cluster(self) -> None:
        """
        choosing random k centroids and then clustering
        """
        # random_list = [1000, 2000, 3000, 4000, 5000]
        for i in range(self.k):
            random_centroid_doc_id = random.randint(0, len(self.document_vertx))
            centroid = self.document_vertx.get(random_centroid_doc_id).term_weight_dict
            cluster = Cluster(centroid)
            self.clusters.append(cluster)
        for document_vertx in self.document_vertx.values():
            most_similar_centroid = self.get_centorid_of_document(document_vertx.term_weight_dict)
            for cluster in self.clusters:
                if cluster.centroid == most_similar_centroid:
                    cluster.members.append(document_vertx)
                    break

    def get_centorid_of_document(self, document_vertex):
        most_similar_centroid = None
        max_cosin_similarity = 0
        for index, cluster in enumerate(self.clusters):
            centoroid_vector = cluster.centroid
            cosin_simi = self.calculate_cosin_similarity(centoroid_vector, document_vertex)
            if cosin_simi > max_cosin_similarity:
                max_cosin_similarity = cosin_simi
                most_similar_centroid = centoroid_vector
        return most_similar_centroid

    @staticmethod
    def calculate_cosin_similarity(doc_vertex1: Dict, doc_vertex2: Dict):

        intersection = set(doc_vertex1.keys()).intersection(doc_vertex2.keys())
        if len(intersection):
            vect1 = [doc_vertex1.get(key) for key in intersection]
            vec2 = [doc_vertex2.get(key) for key in intersection]
            norm_vect_1 = np.linalg.norm(list(doc_vertex1.values()))
            norm_vect_2 = np.linalg.norm(list(doc_vertex2.values()))
            inner_product = pd.Series(vect1).dot(pd.Series(vec2))
            cosin_similarity = inner_product / (norm_vect_1 * norm_vect_2)
            return cosin_similarity
        return 0

    @staticmethod
    def get_document_vertex():
        # return Utils.load_object_from_file('doc_vertex_idf=1').doc_vertex
        data = Utils.load_object_from_file('knn_doc_vertex')
        return data


class Cluster:
    def __init__(self, centroid: Dict):
        self.centroid: Dict = centroid  # a dictionary as centroid
        self.members: List[Vertex] = list()  # list of doc_vertex belong to this cluster


if __name__ == '__main__':
    a = KmeanCluster(k=5)
    # a = Utils.load_object_from_file('a_kmeans')
    for i in range(5):
        a.reassgin()
    print(a)
    print(a)
    print(a)
