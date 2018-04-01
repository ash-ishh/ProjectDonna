# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import warnings
warnings.filterwarnings('ignore', '.*do not.*',)

import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
import string
import numpy as nm
import codecs
import re
import collections
import math
import tensorflow as tf
import random
import glob
import pickle
from os.path import join

def read_file(fileName, allWords):
    file = codecs.open(fileName, encoding='utf-8')
    for line in file:
        line = line.lower().encode('utf-8')
        words = line.split()
        for word in words:
            word = word.translate(None, string.punctuation)
            if word != '':
                allWords.append(word)
    file.close()


def read_file_to_int(dictionary, fileName, allDocuments, allLabels, label):
    file = codecs.open(fileName, encoding='utf-8')
    document = []
    for line in file:
        line = line.lower().encode('utf-8')
        words = line.split()
        for word in words:
            word = word.translate(None, string.punctuation)
            if word in dictionary:
                index = dictionary[word]
            else:
                index = 0  # dictionary['UNK']
            document.append(index)
        allDocuments.append(document)
        allLabels.append(label)
    file.close()


def build_dataset(words):
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
    dictionary = dict()
    data = list()
    unk_count = 0

    for word, _ in count:
        dictionary[word] = len(dictionary)

    for word in words:
        if word in dictionary:
            index = dictionary[word]
    else:
        index = 0  # dictionary['UNK']
        unk_count = unk_count + 1

    data.append(index)
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return dictionary, reverse_dictionary


def pre_process(train_dir):
    #Global Initializarion
    global vocabulary_size
    vocabulary_size = 20000
    allWords = []
    allDocuments = []
    allLabels = []
    #Each word of negative reviews is appended to AllWords
    fileList = glob.glob(join(train_dir,"neg/*.txt"))
    for file in fileList:
        read_file(file, allWords)

    fileList = glob.glob(join(train_dir,"pos/*.txt"))
    for file in fileList:
        read_file(file, allWords)

    dictionary, reverse_dictionary = build_dataset(allWords)
    dictionary_f = open("data/dict.pkl","wb")
    pickle.dump(dictionary,dictionary_f)
    print(len(dictionary))
    print(len(reverse_dictionary))

    del allWords  # Hint to reduce memory.

    fileList = glob.glob(join(train_dir,"neg/*.txt"))
    for file in fileList:
        read_file_to_int(dictionary, file, allDocuments, allLabels, 0)

    print("Len : fileList , allDocs , allLabels")
    print(len(fileList))
    print(len(allDocuments))
    print(len(allLabels))

    fileList = glob.glob(join(train_dir,"pos/*.txt"))
    for file in fileList:
        read_file_to_int(dictionary, file, allDocuments, allLabels, 1)

    print("Len : fileList , allDocs , allLabels")
    print(len(fileList))
    print(len(allDocuments))
    print(len(allLabels))
    c = list(zip(allDocuments, allLabels)) # shuffle them partitioning
    random.shuffle(c)

    allDocuments, allLabels = zip(*c)
    return allDocuments,allLabels


def train(allDocuments,allLabels):
    a = raw_input("Press Enter to continue training..")
    trainX = allDocuments[:22500]
    testX = allDocuments[22500:]

    trainY = allLabels[:22500]
    testY = allLabels[22500:]

    trainX = pad_sequences(trainX, maxlen=100, value=0.)
    testX = pad_sequences(testX, maxlen=100, value=0.)

    # Converting labels to binary vectors
    trainY = to_categorical(trainY, nb_classes=2)
    testY = to_categorical(testY, nb_classes=2)

    # Network building
    net = tflearn.input_data([None, 100])
    net = tflearn.embedding(net, input_dim=vocabulary_size, output_dim=128)
    net = tflearn.lstm(net, 128, dropout=0.8)
    net = tflearn.fully_connected(net, 2, activation='softmax')
    net = tflearn.regression(net, optimizer='adam', learning_rate=0.001,loss='categorical_crossentropy')

    # Training
    model = tflearn.DNN(net, tensorboard_verbose=0)
    model.fit(trainX, trainY, validation_set=(testX, testY), show_metric=True,batch_size=32)
    model.save("sentimental_analysis_model.tfl")
    score = model.evaluate(testX,testY)
    print(score)

if __name__ == "__main__":
    allDocuments , allLabels = pre_process("data/aclImdb/train")
    train(allDocuments , allLabels)
