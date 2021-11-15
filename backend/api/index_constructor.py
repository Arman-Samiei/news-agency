from api.basic_text_processes import text_processing,get_learning_datas,remove_punctuation

def index_constructor(news, file_name):
    learning_words = get_learning_datas()
    index = {}
    is_doc_in_index = False
    num_of_docs = len(news)
    for i ,n in enumerate(news):
        text = remove_punctuation(n.text)
        title = remove_punctuation(n.title)
        text.extend(title)
        for word in text:
            word = text_processing(word,learning_words)
            if word is None:
                continue
            elif not word in index:
                index[word] = [(n.id, 1)]
            else:
                for i,(doc_id,tf) in enumerate(index[word]):
                    if doc_id == n.id:
                        index[word][i] = (doc_id, tf + 1)
                        is_doc_in_index = True
                        break
                if not is_doc_in_index:
                    index[word].append((n.id, 1))
            is_doc_in_index = False
    with open(file_name, 'w', encoding="utf-8") as writer:
        writer.write(f'{num_of_docs}\n')
        for word, postings_list in index.items():
            writer.write(f'{word} {postings_list}\n')