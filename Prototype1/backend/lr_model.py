import re
import joblib
import numpy as np
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load once
stop = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load model and vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")
model = joblib.load("logistic_model.pkl")

# Preprocessing
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = ' '.join([word for word in text.split() if word not in stop])
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

# Sentiment score (optional if used during training)
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Predict function
def predict_text(text):
    cleaned = preprocess(text)
    sentiment = get_sentiment(cleaned)
    title_length = len(cleaned)
    
    # Combine features manually as done during training
    df = {"text": [cleaned], "sentiment": [sentiment], "title_length": [title_length]}
    
    # Vectorize text
    text_features = vectorizer.transform([cleaned])
    
    # Predict
    prediction = model.predict(text_features)[0]
    return "fake" if prediction == 0 else "real"

