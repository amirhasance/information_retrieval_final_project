import pickle

import parsivar

from Index.positional.DocTerm import Term
from my_tokenizer.m_tokenizer import get_token_stream
with open("docid_to_doc_title", 'rb') as file_:
    doc_id_to_doc_title = pickle.load(file_)
with open("backup_file_Without_StopWords" , 'rb') as file_:
    data_dict = pickle.load(file_)


def index():
    global data_dict
    global doc_id_to_doc_title
    for doc_id, words, doc_title in get_token_stream:
        for position, word in enumerate(words):
            if word not in data_dict.keys():
                data_dict[word] = Term(id=id(word))
            data_dict[word].insert(doc_id=doc_id, position=position)
        doc_id_to_doc_title[doc_id] = doc_title

    return data_dict, doc_id_to_doc_title



def search_one_word(word):
    global data_dict
    word = parsivar.Normalizer().normalize(word)
    sterm = parsivar.FindStems().convert_to_stem(word)
    doc_id_list = data_dict.get(sterm).docTerms.keys()
    return doc_id_list


def query(two_part_word) -> set:
    # data_dict = data_index
    global data_dict
    global doc_id_to_doc_title
    normalized_input = parsivar.Normalizer().normalize(two_part_word)
    tokens = parsivar.Tokenizer().tokenize_words(normalized_input)
    word1 = tokens[0]
    word1 = parsivar.FindStems().convert_to_stem(word1)
    word2 = tokens[1]
    word2 = parsivar.FindStems().convert_to_stem(word2)
    doc_id_list_word1 = data_dict.get(word1).docTerms.keys()
    doc_id_list_word2 = data_dict.get(word2).docTerms.keys()

    iter_doc_id_word1 = iter(doc_id_list_word1)
    iter_doc_id_word2 = iter(doc_id_list_word2)
    final_found_doc_id_set = set()
    try:
        doc_id_word1 = next(iter_doc_id_word1)
        doc_id_word2 = next(iter_doc_id_word2)
        while True:
            if doc_id_word1 == doc_id_word2:
                same_doc_id = doc_id_word2
                position_list_word1 = data_dict.get(word1).docTerms[same_doc_id].positions
                positions_list_word2 = data_dict.get(word2).docTerms[same_doc_id].positions
                for position_word1 in position_list_word1:
                    if position_word1 + 1 in positions_list_word2:
                        final_found_doc_id_set.add(same_doc_id)
                        break
                doc_id_word2 = next(iter_doc_id_word2)
                doc_id_word1 = next(iter_doc_id_word1)
            elif doc_id_word1 > doc_id_word2:
                doc_id_word2 = next(iter_doc_id_word2)
            else:
                doc_id_word1 = next(iter_doc_id_word1)

    except Exception as e:
        pass
    return final_found_doc_id_set


def main_query(input_query):
    global data_dict
    global doc_id_to_doc_title
    normalized_input = parsivar.Normalizer().normalize(input_query)
    tokens = parsivar.Tokenizer().tokenize_words(normalized_input)
    number_of_tokens = len(tokens)

    all_p1p2_list = []
    if number_of_tokens > 2:
        for index in range(number_of_tokens - 1):
            all_p1p2_list.append(query(tokens[index] + " " + tokens[index + 1]))

        len_ = number_of_tokens
        ranked_dict = {}
        while len_ > 2:

            for i in range(number_of_tokens - len_ + 1):
                shared_list = set(all_p1p2_list[i]).intersection(all_p1p2_list[i + 1])
                ranked_list = shared_list.copy()
                for j in range(i + 2, i + len_ - 1):
                    shared_list = set(shared_list).intersection(all_p1p2_list[j])
                    ranked_list.extend(shared_list)

                ranked_dict[len_] = ranked_list
            len_ -= 1
        ranked_list = []
        for i in range(number_of_tokens - 1):
            shared_list = all_p1p2_list[i]
            ranked_list.extend(shared_list)
        ranked_dict[2] = set(ranked_list)
        return ranked_dict
    elif number_of_tokens == 2:
        return query(normalized_input)
    else:
        return search_one_word(tokens[0])


if __name__ == '__main__':

    main_query("واکسن آسترازنکا")
