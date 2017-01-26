data = get_data()

def get_data():

    from keras.preprocessing import sequence
    from keras.datasets import imdb

    max_features = 5000
    maxlen = 500

    (X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)

    return {
        'train': {
            'in': {
                'input': X_train,
            },

            'out': {
                'output': y_train,
            },
        },

        'test': {
            'in': {
                'input': X_test,
            },

            'out': {
                'output': y_test,
            },
        },
    }
