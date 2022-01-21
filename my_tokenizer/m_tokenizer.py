import os.path
from typing import Tuple, List
from adapter.adapter import get_doc_id_and_document, KnnAdapter, Doc
from parsivar import Normalizer, Tokenizer, FindStems


class MyTokenizer:
    def __init__(self, stop_word: bool = False, stemming: bool = True):
        self.stop_word = stop_word
        self.stemming = stemming
        self.stop_words = self.get_stop_words()
        self.docs = get_doc_id_and_document
        self.stemer = FindStems().convert_to_stem

    def get_tokenized_stream(self) -> Tuple:
        for doc_id, document, doc_title in self.docs:
            normalized_document: str = Normalizer().normalize(document)
            token_words: List = Tokenizer().tokenize_words(normalized_document)
            tokens = list()
            for word_ in token_words:
                word = word_
                if self.stemming:
                    word = self.stemer(word)
                if not self.stop_word and word in self.stop_words:
                    pass
                else:
                    tokens.append(word)

            yield doc_id, tokens, doc_title

    @staticmethod
    def get_stop_words() -> List:
        base_dir = os.path.dirname(__file__)
        file_name = "stopwords.dat"
        with open(os.path.join(base_dir, file_name), 'r') as file_p:
            stop_word_list = file_p.readlines()
            stop_word_list = [stopword.replace("\n", "") for stopword in stop_word_list]
        return stop_word_list


class KnnTokenizer(MyTokenizer):
    def __init__(self):
        super().__init__()
        self.docs: List[Doc] = KnnAdapter().get_doc_id_and_documents()

    def get_tokenized_stream(self) -> List[Tuple[List, Doc]]:
        for doc in self.docs:
            try:
                normalized_document: str = Normalizer().normalize(doc.content)
                token_words: List = Tokenizer().tokenize_words(normalized_document)
                tokens = list()
                for word_ in token_words:
                    word = word_
                    if self.stemming:
                        word = self.stemer(word)
                    if not self.stop_word and word in self.stop_words:
                        pass
                    else:
                        tokens.append(word)
                yield tokens, doc
            except Exception as e:
                print(e)


get_token_stream = MyTokenizer().get_tokenized_stream()
