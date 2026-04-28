import numpy as np
from pickle import load
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import random
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.xception import Xception, preprocess_input
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, add
from tensorflow.keras.models import Model


tokenizer = load(open("tokenizer.pkl", "rb"))
max_length = 35
vocab_size = len(tokenizer.word_index) + 1

def define_model(vocab_size, max_length):
    inputs1 = Input(shape=(2048,))
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation='relu')(fe1)

    inputs2 = Input(shape=(max_length,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)

    decoder1 = add([fe2, se3])
    decoder2 = Dense(256, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    return model

model = define_model(vocab_size, max_length)
model.load_weights("model.h5")

xception_model = Xception(include_top=False, pooling="avg")

def extract_features(filename):
    image = load_img(filename, target_size=(299, 299))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    feature = xception_model.predict(image, verbose=0)
    return feature

def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo, sequence], verbose=0)
        pred = np.random.choice(len(pred[0]), p=pred[0])
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text

image_folder = "Images"

all_images = os.listdir(image_folder)
img_name = random.choice(all_images)

img_path = os.path.join(image_folder, img_name)

print("Selected Image:", img_name)

photo = extract_features(img_path)
description = generate_desc(model, tokenizer, photo, max_length)

print("RAW:", description)

words = description.split()

filtered = []
for w in words:
    if w not in ["startseq", "endseq"]:
        if len(filtered) == 0 or w != filtered[-1]:
            filtered.append(w)

sentence = " ".join(filtered)
sentence = sentence.capitalize()

print("Caption:", sentence)