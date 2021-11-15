import re
import math
import os
from django.conf import settings

def get_docs_tfs(input_string):
    first_bracket_pos = input_string.find('[')

    docs = re.findall(r'\d{1,}', input_string[first_bracket_pos + 1:-2:1])[0::2]
    tfs = re.findall(r'\d{1,}', input_string[first_bracket_pos + 1:-2:1])[1::2]
    for j in range(len(docs)):
        docs[j] = int(docs[j])
        tfs[j] = int(tfs[j])
    return docs, tfs


def calculate_df_tf(refined_query, line_word, df_for_each_term_in_query, docs, tf_document_term, tfs):
    for word in refined_query:
        if word == line_word:
            if not word in df_for_each_term_in_query:
                df_for_each_term_in_query[word] = len(docs)
            else:
                df_for_each_term_in_query[word] += len(docs)
            for l, doc in enumerate(docs):
                if not doc in tf_document_term:
                    tf_document_term[doc] = [(word, tfs[l])]
                else:
                    tf_document_term[doc].append((word, tfs[l]))
            break
    return df_for_each_term_in_query, tf_document_term


def calculate_docs_length_power_two(docs, tfs, docs_length, word):
    for k, doc in enumerate(docs):
        if not doc in docs_length:
            docs_length[doc] = tfs[k] ** 2
        else:
            docs_length[doc] += tfs[k] ** 2
    return docs_length


def calculate_query_tf_idf(refined_query, df_for_each_term_in_query, num_of_docs):
    for word in refined_query:
        if not word in df_for_each_term_in_query:
            df_for_each_term_in_query[word] = 0
        if df_for_each_term_in_query[word] == 0:
            df_for_each_term_in_query[word] = num_of_docs
        wtq = (1 + math.log(refined_query[word], 10)) * math.log(num_of_docs / df_for_each_term_in_query[word], 10)
        refined_query[word] = wtq
    return refined_query


def handle_indexes(file_name, num_of_docs, scores, docs_length, refined_query, df_for_each_term_in_query,
                   tf_document_term):
    with open(file_name, encoding='utf-8') as fp:
        for i, line in enumerate(fp):
            if i == 0:
                num_of_docs += int(line)
                continue
            docs, tfs = get_docs_tfs(line)
            for doc in docs:
                if not doc in scores:
                    scores[doc] = 0
            docs_length = calculate_docs_length_power_two(docs, tfs, docs_length, line.split(' ')[0])
            df_for_each_term_in_query, tf_document_term = calculate_df_tf(refined_query, line.split(' ')[0],
                                                                          df_for_each_term_in_query, docs,
                                                                          tf_document_term, tfs)
    return num_of_docs, scores, docs_length, df_for_each_term_in_query, tf_document_term

def calculate_doc_scores(tf_document_term, scores, refined_query, docs_length):
    for doc in tf_document_term:
        for (word, tf) in tf_document_term[doc]:
            if not doc in scores:
                scores[doc] = refined_query[word] * (1 + math.log(tf, 10)) / docs_length[doc]
            else:
                scores[doc] += refined_query[word] * (1 + math.log(tf, 10)) / docs_length[doc]
    return scores