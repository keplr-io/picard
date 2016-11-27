from keras.preprocessing.text import Tokenizer
from pandas import Series

def process_text_seq(df):
    tokenizer = Tokenizer(nb_words=500)

    texts = df.tolist()

    tokenizer.fit_on_texts(texts)
    result = tokenizer.texts_to_matrix(texts, 'count')

    return result
