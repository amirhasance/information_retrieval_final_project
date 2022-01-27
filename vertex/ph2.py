from my_index.non_positional.index import Index
from utils.utils import Utils
from vertex.doc_vertex import DocumentsVertex

inverted_index = Utils.load_object_from_file('non_pos_inverted_index')
doc_vertex = Utils.load_object_from_file("doc_vertex_idf=1")
doc_id_to_doc_title = Utils.load_object_from_file("doc_id_to_doc_title")
document_vertex = DocumentsVertex(index=inverted_index, doc_vertex=doc_vertex.doc_vertex,
                                  doc_id_to_doc_title=doc_id_to_doc_title)




query = "واکسن"

ans = document_vertex.get_ranked_result(query)
query = "دانشگاه صنعتی امیرکبیر"
ans = document_vertex.get_ranked_result(query)
query = "ژیمناستیک"

ans = document_vertex.get_ranked_result(query)
query = "مجموع بیمار کویید"

ans = document_vertex.get_ranked_result(query)

# document_vertex.create_weighted_vertex()
# Utils.save_object_to_file(document_vertex, "document_vertex")
