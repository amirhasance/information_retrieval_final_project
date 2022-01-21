import os
from collections import namedtuple
from typing import List

import pandas as pd

from utils.utils import Utils


class Adapter:
    base_dir = os.path.dirname(__file__)
    file_name = "IR1_7k_news.xlsx"
    data_path = os.path.join(base_dir, file_name)

    def read_excel_file(self):
        df = pd.read_excel(self.data_path)
        return df

    def get_doc_id_and_documents(self):
        df = self.read_excel_file()
        for doc_id, document in enumerate(df.values):
            yield doc_id, document[0], document[2]

    def get_number_of_doc(self):
        df = self.read_excel_file()
        return len(df.values)

    def save_doc_id_to_doc_title(self):
        doc_id_to_doc_title = dict()
        for doc_id, document, doc_title in get_doc_id_and_document:
            doc_id_to_doc_title[doc_id] = doc_title
        Utils.save_object_to_file(doc_id_to_doc_title, "doc_id_to_doc_title")


N = Adapter().get_number_of_doc()
get_doc_id_and_document = Adapter().get_doc_id_and_documents()

Doc = namedtuple("Doc", ['doc_id', 'doc_title', 'catergory', 'content'])


class KnnAdapter(Adapter):
    file_names = ['IR00_3_11k News.xlsx', 'IR00_3_17k News.xlsx', 'IR00_3_20k News.xlsx']
    base_dir = os.path.join(Adapter.base_dir, '..', 'KNN', 'train_set')

    def __init__(self):
        self.data_path = [os.path.join(self.base_dir, file_name) for file_name in self.file_names]
        super().__init__()

    def read_excel_file(self):
        for data_pth in self.data_path:
            df = pd.read_excel(data_pth)
            yield df

    def get_doc_id_and_documents(self) -> List[Doc]:
        doc_id = 0
        Doc = namedtuple("Doc", ['doc_id', 'doc_title', 'catergory', 'content'])
        for df in self.read_excel_file():
            for document in df.values:
                doc = Doc(doc_id, document[3], document[2], document[1])
                yield doc
                doc_id += 1

    def get_number_of_doc(self):
        n = 0
        for df in self.read_excel_file():
            n += len(df.values)
        return n


if __name__ == '__main__':
    # Adapter().save_doc_id_to_doc_title()
    print(list(KnnAdapter().get_doc_id_and_documents()))
