

import numpy as np
from pickle import load
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, add
from tensorflow.keras.models import Model

# load features
features = load(open("features.pkl", "rb"))

# load descriptions
def load_clean_descriptions(filename):
    file = open(filename, 'r')
    doc = file.read()
    file.close()

    descriptions = dict()
    for line in doc.split('\n'):
        tokens = line.split()
        if len(tokens) < 2:
            continue

        image_id, image_desc = tokens[0], tokens[1:]

        if image_id not in descriptions:
            descriptions[image_id] = list()

        desc = 'startseq ' + ' '.join(image_desc) + ' endseq'
        descriptions[image_id].append(desc)

    return descriptions

descriptions = load_clean_descriptions("descriptions.txt")


def to_lines(descriptions):
    all_desc = list()
    for key in descriptions.keys():
        [all_desc.append(d) for d in descriptions[key]]
    return all_desc

def create_tokenizer(descriptions):
    lines = to_lines(descriptions)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)
    return tokenizer

tokenizer = create_tokenizer(descriptions)
from pickle import dump
dump(tokenizer, open("tokenizer.pkl", "wb"))
vocab_size = len(tokenizer.word_index) + 1

# max length
def max_length(descriptions):
    lines = to_lines(descriptions)
    return max(len(d.split()) for d in lines)

max_len = max_length(descriptions)


def create_sequences(tokenizer, max_len, desc_list, photo):
    X1, X2, y = list(), list(), list()

    photo = np.array(photo).reshape(2048)

    for desc in desc_list:
        seq = tokenizer.texts_to_sequences([desc])[0]

        for i in range(1, len(seq)):
            in_seq, out_seq = seq[:i], seq[i]

            in_seq = pad_sequences([in_seq], maxlen=max_len)[0]
            out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]

            X1.append(photo)
            X2.append(in_seq)
            y.append(out_seq)

    return np.array(X1), np.array(X2), np.array(y)


def data_generator(descriptions, photos, tokenizer, max_len):
    batch_size = 64

    while True:
        X1, X2, y = [], [], []

        for key, desc_list in descriptions.items():
            if key not in photos:
                continue

            photo = photos[key]
            photo = np.array(photo).reshape(2048)

            X1_temp, X2_temp, y_temp = create_sequences(tokenizer, max_len, desc_list, photo)

            for i in range(len(X1_temp)):
                X1.append(X1_temp[i])
                X2.append(X2_temp[i])
                y.append(y_temp[i])

                if len(X1) == batch_size:
                    yield ((np.array(X1), np.array(X2)), np.array(y))
                    X1, X2, y = [], [], []


def define_model(vocab_size, max_len):
    inputs1 = Input(shape=(2048,))
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation='relu')(fe1)

    inputs2 = Input(shape=(max_len,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)

    decoder1 = add([fe2, se3])
    decoder2 = Dense(256, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    print(model.summary())
    return model

model = define_model(vocab_size, max_len)

epochs = 20
steps = 100  

generator = data_generator(descriptions, features, tokenizer, max_len)

model.fit(generator, epochs=epochs, steps_per_epoch=steps)

model.save("model.h5")

print("TRAINING COMPLETE")