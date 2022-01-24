from time import time

from KNN.knn import DocumentsVertex

cat_query = {'political': "مذاکره", 'economy': "بودجه", \
             'sports': "استقلال", 'health': "کرونا", 'culture': "شاعر"}
obj = DocumentsVertex()
for cat, query in cat_query.items():
    # candid_document from category
    print('category = ', cat)
    query_posting_list = obj.inverted_index.get(query)
    print("select from its category")
    start_time = time()
    candid_docs = []
    term_id = obj.term_to_termid.get(query)
    in_category_candid_docs = [doc for doc in obj.doc_vertex.values() if obj.doc_id_to_category.get(doc.doc_di) == cat]
    for doc_vertx in in_category_candid_docs:
        weight_of_query_in_vertex = doc_vertx.term_weight_dict.get(query)
        if weight_of_query_in_vertex:
            doc_id = doc_vertx.doc_id
            if doc_id in query_posting_list.keys():
                candid_docs.append(doc_vertx)
    candid_docs.sort(key=lambda x: x.term_weight_dict.get(term_id))
    print(time() - start_time)
    print("select from posting")
    candid_docs = []
    for posting in query_posting_list:
        doc_id = posting.docId
        doc_vertx = obj.doc_vertex.get(doc_id)
        if term_id in doc_vertx.term_weight_dict.keys():
            candid_docs.append(doc_vertx)
    candid_docs.sort(key=lambda x: x.term_weight_dict.get(term_id))






    pass
