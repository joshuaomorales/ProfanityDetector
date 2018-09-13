#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Google Vision API
import io
import os

# set credentials (IMPORTANT)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\apikey.json'

from google.cloud import vision
from google.cloud.vision import types

# NLTK for tokenization and stop words removal
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# Open text files needed
google_banned_bad_words = open("../Profanity/Google Profanity.txt", "r").read()

google_dictionary = []
for w in google_banned_bad_words.split('\n'):
    google_dictionary.append(w.replace(" ","-"))

# Detected
detected_profanity_files = []

def vision_detect_text(path):

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image)
    texts = response.full_text_annotation

    #output = texts.text.encode("utf-8")
    output = texts.text

    return output

def lower_letter_case(tokens):
    lowercase_tokens = []
    for t in tokens:
        lowercase_tokens.append(t.lower())
    return lowercase_tokens

def tokenize(sentence):
    tokens = word_tokenize(sentence)
    return lower_letter_case(tokens)

def remove_stopwords(tokens):
    filtered_words = []
    stopWords = set(stopwords.words("english"))
    for w in tokens:
        if w not in stopWords:
            filtered_words.append(w)
    return filtered_words

def preprocess(detected_text):
    tokens = tokenize(detected_text)
    filtered_words = remove_stopwords(tokens)
    return remove_punctuations(filtered_words)

def remove_punctuations(tokens):
    tokenizer = RegexpTokenizer(r'\w+')
    filtered_words = []
    for t in tokens:
            for t in tokenizer.tokenize(t):
                filtered_words.append(t)
    return(filtered_words)

def check_profanity(file_name):
    print file_name
    google_banned_matched = []

    vision_detected_text = vision_detect_text(file_name)
    vision_preprocessed_text = preprocess(vision_detected_text)
    tokens = vision_preprocessed_text
    
    for token in tokens:
        for bad_word in google_dictionary:
           if token == bad_word:
               google_banned_matched.append(token)
               break
        
    if len(google_banned_matched) > 0:
        detected_profanity_files.append(file_name)
        print("Detected profane terms: "+ str(google_banned_matched))

if __name__ == "__main__":


    for x in range(1,51):
        file_name = "../NonOffensiveImages/" + str(x) + ".jpg"
        check_profanity(file_name)
    print("Total No. of Images with Profanity: " + str(len(detected_profanity_files)) )
    print(len(detected_profanity_files))
   
