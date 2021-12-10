from Index.non_positional.Index import Index
from utils.utils import Utils
from vertex.doc_vertex import DocumentsVertex

inverted_index = Utils.load_object_from_file('non_pos_inverted_index')
doc_vertex = Utils.load_object_from_file("document_vertex")
document_vertex = DocumentsVertex(index=inverted_index, doc_vertex=doc_vertex)
query = "دانشگاه صنعتی امیرکبیر"
ans = document_vertex.get_ranked_result(query)
print(ans)
# document_vertex.create_weighted_vertex()
# Utils.save_object_to_file(document_vertex, "document_vertex")
