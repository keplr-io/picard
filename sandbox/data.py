def get_data():

    from keras.preprocessing import sequence
    from keras.datasets import imdb

    max_features = 5000
    maxlen = 105

    (X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)

    return {
        'train': {
            'in': {
                'headline-input': X_train[:, :100],
                'aux-input': X_train[:, -5 :],
            },

            'out': {
                'headline-output': y_train[:],
                'aux-output': y_train[:],
            },
        },

        'test': {
            'in': {
                'headline-input': X_test[:, :100],
                'aux-input': X_test[:, -5 :],
            },

            'out': {
                'headline-output': y_test[:],
                'aux-output': y_test[:],
            },
        },
    }
