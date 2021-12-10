import os

import pandas as pd


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


N = Adapter().get_number_of_doc()
get_doc_id_and_document = Adapter().get_doc_id_and_documents()


if __name__ == '__main__':
    print(N)