#!/usr/bin/env python
# coding: utf-8

import warnings

warnings.filterwarnings("ignore")
import os
import matplotlib.pyplot as plt
import pandas as pd
from models.text_cnn import  build_text_cnn
from config import *
from utils.preprocessing import *

base_dir = os.path.curdir
file_list = [train_file_path, valid_file_path, test_file_path]
for i, filename in enumerate(file_list):
    file_list[i] = os.path.join(
        os.path.abspath(base_dir), filename)

build_vocab(filenames=file_list, vocab_dir=vocab_dir, vocab_size=vocab_size)

words, word_to_id = read_vocab(vocab_dir)
categories, cat_to_id = read_category()

vocab_size = len(words)

vector_word_filename = 'vector_word.txt'  # vector_word trained by word2vec
train_word2vec(file_list, vector_word_filename)
vector_word_npz = 'vector_word.npz'  # save vector_word to numpy file
# trans vector file to numpy file
if not os.path.exists(vector_word_npz):
    export_word2vec_vectors(word_to_id,
                            vector_word_filename,
                            vector_word_npz)
pre_trianing = get_training_word2vec_vectors(vector_word_npz)

train_file_name = "sample__train_0.2.txt"
x_train, y_train = process_file(train_file_name,
                                word_to_id,
                                cat_to_id,
                                max_length=max_length)

valid_file_name = "sample__valid_0.2.txt"
x_valid, y_valid = process_file(valid_file_name,
                                word_to_id,
                                cat_to_id, max_length=max_length)

y_train = y_train.astype("int")

train_embedding = get_training_word2vec_vectors("vector_word.npz")

model = build_text_cnn(x_train=x_train, embedding_matrix=train_embedding)

history = model.fit(x_train,
                    y_train,
                    batch_size=64,
                    epochs=20,
                    validation_data=(x_valid, y_valid))

model.save("cnews_classfication_10.h5")


def plot_learning_curves(history):
    pd.DataFrame(history.history).plot(figsize=(8, 5))
    plt.grid(True)
    plt.gca().set_ylim(0, 2)
    plt.savefig('loss.png')
    plt.show()


plot_learning_curves(history)