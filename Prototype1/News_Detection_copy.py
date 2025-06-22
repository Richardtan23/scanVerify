#!/usr/bin/env python
# coding: utf-8

# Import Libraries
import pandas as pd
import numpy as np
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from textblob import TextBlob
import joblib  # For saving/loading model and vectorizer

# Load Datasets
dFrame_fake = pd.read_csv("Fake.csv")
dFrame_true = pd.read_csv("True.csv")
dFrame_true["text"] = dFrame_true["text"].replace("(Reuters)", "", regex=True)

# Assign Labels
dFrame_fake["target"] = 0
dFrame_true["target"] = 1

# Drop Unused Columns
dFrame_fake = dFrame_fake.drop(["subject", "date"], axis=1)
dFrame_true = dFrame_true.drop(["subject", "date"], axis=1)

# Load and Clean Additional Dataset
dFrame_new = pd.read_csv("news.csv")
dFrame_new = dFrame_new.drop(columns=['Unnamed: 0'], errors='ignore')
dFrame_new.columns = dFrame_new.columns.str.strip().str.lower()
dFrame_new['target'] = dFrame_new['label'].apply(lambda x: 1 if x.upper() == 'REAL' else 0)
dFrame_new = dFrame_new[['title', 'text', 'target']]

# Combine All Data
dFrame = pd.concat([dFrame_fake, dFrame_true, dFrame_new], axis=0).reset_index(drop=True)

# Text Cleaning Functions
def wordopt(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub('[()]','',text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_title(title):
    title = title.lower()
    title = re.sub(r'\[.*?\]|\(.*?\)', '', title)
    title = re.sub(r'https?://\S+|www\.\S+', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

dFrame["text"] = dFrame["text"].apply(wordopt)
dFrame['title'] = dFrame['title'].apply(clean_title)

# Add Features
dFrame['sentiment'] = dFrame['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
dFrame['title_length'] = dFrame['title'].apply(len)
dFrame['text_length'] = dFrame['text'].apply(len)
dFrame['exclamation_count'] = dFrame['text'].apply(lambda x: x.count('!'))

# Train/Test Split
X = dFrame[['text', 'sentiment', 'title_length']]
y = dFrame['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorization
tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english', analyzer='word', sublinear_tf=True)
X_train_tfidf = tfidf.fit_transform(X_train['text'])
X_test_tfidf = tfidf.transform(X_test['text'])

# Save TF-IDF Vectorizer
joblib.dump(tfidf, "tfidf_vectorizer.pkl")

# Logistic Regression Training
lr = LogisticRegression(class_weight='balanced', random_state=42)
lr.fit(X_train_tfidf, y_train)

# Save Logistic Regression Model
joblib.dump(lr, "logistic_model.pkl")

# Evaluation
y_pred_lr = lr.predict(X_test_tfidf)
print("Logistic Regression Performance:")
print(classification_report(y_test, y_pred_lr))

# Manual Testing Function
def output_label(n):
    return "Real News" if n == 1 else "Fake News"

def manual_testing(news):
    tfidf_loaded = joblib.load("tfidf_vectorizer.pkl")
    model_loaded = joblib.load("logistic_model.pkl")
    test_df = pd.DataFrame({"text": [news]})
    test_df["text"] = test_df["text"].apply(wordopt)
    transformed = tfidf_loaded.transform(test_df["text"])
    prediction = model_loaded.predict(transformed)
    print("\nLogistic Regression Prediction: {}".format(output_label(prediction[0])))

# Input
if __name__ == "__main__":
    news = input("Enter news text: ")
    manual_testing(news)


