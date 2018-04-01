# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import pad_sequences
import string
import pickle

def read_file_to_int(dictionary,sentence,word_count):
    sentence = sentence.lower().encode('utf-8')
    words = sentence.split()
    document = []
    for word in words:
        word = word.translate(None,string.punctuation)
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0
        document.append(index)
    word_count.append(document)

dictionary_f = open("data/dict.pkl","rb")
dictionary = pickle.load(dictionary_f)

net = tflearn.input_data([None,100])
net = tflearn.embedding(net,input_dim=10000,output_dim =128)
net = tflearn.lstm(net,128,dropout=0.8)
net = tflearn.fully_connected(net,2,activation="softmax")
net = tflearn.regression(net,optimizer="adam",learning_rate=0.0001, loss="categorical_crossentropy")
model = tflearn.DNN(net,tensorboard_verbose=0)
model.load("sentimental_analysis_model.tfl")

while True:
    sentence = raw_input("Hey How You Doin'?\n")
    word_count = []
    read_file_to_int(dictionary,sentence,word_count)
    predict_input = pad_sequences(word_count,maxlen=100,value=0.)
    p = model.predict(predict_input)
    neg = p[0][0]
    pos = p[0][1]

    print("Negative Percentage : " , neg*100)
    print("Positive Percentage : " , pos*100)
    print("\n\n")
