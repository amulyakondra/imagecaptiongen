import os
import numpy as np
import string
import matplotlib.pyplot as plt

from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, add
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical


# -------------------------
# IMAGE FEATURE EXTRACTION
# -------------------------
def extract_features(image_dir):
    model = ResNet50(weights='imagenet')
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)

    features = {}

    for img in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img)

        image = load_img(img_path, target_size=(224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)

        feature = model.predict(image, verbose=0)
        img_id = img.split('.')[0]
        features[img_id] = feature

    return features


# -------------------------
# LOAD CAPTIONS
# -------------------------
def load_captions(file_path):
    captions = {}

    with open(file_path, 'r') as f:
        for line in f:
            tokens = line.strip().split(',')

            if len(tokens) < 2:
                continue

            img_id, caption = tokens[0], tokens[1]
            img_id = img_id.split('.')[0]

            captions.setdefault(img_id, []).append(caption)

    return captions


# -------------------------
# CLEAN TEXT
# -------------------------
def clean_captions(captions):
    table = str.maketrans('', '', string.punctuation)

    for key in captions:
        for i in range(len(captions[key])):
            cap = captions[key][i].lower()
            cap = cap.translate(table)
            cap = ' '.join([w for w in cap.split() if len(w) > 1])
            captions[key][i] = "startseq " + cap + " endseq"


# -------------------------
# TOKENIZER
# -------------------------
def create_tokenizer(captions):
    lines = []
    for k in captions:
        lines.extend(captions[k])

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)

    return tokenizer


# -------------------------
# MODEL
# -------------------------
def define_model(vocab_size, max_length):
    inputs1 = Input(shape=(2048,))
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation='relu')(fe1)

    inputs2 = Input(shape=(max_length,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)

    decoder = add([fe2, se3])
    decoder = Dense(256, activation='relu')(decoder)
    outputs = Dense(vocab_size, activation='softmax')(decoder)

    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model


# -------------------------
# CAPTION GENERATION
# -------------------------
def generate_caption(model, tokenizer, photo, max_length):
    in_text = "startseq"

    for _ in range(max_length):
        seq = tokenizer.texts_to_sequences([in_text])[0]
        seq = pad_sequences([seq], maxlen=max_length)

        yhat = model.predict([photo, seq], verbose=0)
        yhat = np.argmax(yhat)

        word = None
        for w, idx in tokenizer.word_index.items():
            if idx == yhat:
                word = w
                break

        if word is None:
            break

        in_text += " " + word

        if word == "endseq":
            break

    return in_text


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":

    IMAGE_DIR = "dataset/images"
    CAPTION_FILE = "dataset/captions.txt"

    print("Extracting features...")
    features = extract_features(IMAGE_DIR)

    print("Loading captions...")
    captions = load_captions(CAPTION_FILE)

    print("Cleaning captions...")
    clean_captions(captions)

    print("Creating tokenizer...")
    tokenizer = create_tokenizer(captions)

    vocab_size = len(tokenizer.word_index) + 1
    max_length = max(len(c.split()) for k in captions for c in captions[k])

    print("Building model...")
    model = define_model(vocab_size, max_length)

    print("Training model...")
    model.fit(
        x=[np.zeros((1,2048)), np.zeros((1,max_length))],
        y=np.zeros((1, vocab_size)),
        epochs=1
    )

    print("Done (demo run)")