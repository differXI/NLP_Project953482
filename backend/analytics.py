import joblib

vectorizer = joblib.load("models/vectorizer.pkl")
sentiment_model = joblib.load("models/sentiment_model.pkl")
category_model = joblib.load("models/category_model.pkl")
mlb = joblib.load("models/mlb.pkl")

def analyze_text(text: str):
    X = vectorizer.transform([text])
    sent = sentiment_model.predict(X)[0]
    cats = mlb.inverse_transform(category_model.predict(X))[0]
    return sent, list(cats)
