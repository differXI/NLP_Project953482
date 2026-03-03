import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

def load_and_prepare_data():
    """
    Load comments และสร้าง labels สำหรับ sentiment

    Labeling Strategy:
    - Positive: rating >= 4.0
    - Neutral: 3.0 <= rating < 4.0
    - Negative: rating < 3.0

    Returns:
        X: list of comments
        y: list of sentiment labels
    """
    df = pd.read_csv("data/RateMyProfessor_Sample.csv")
    df = df[['star_rating', 'comments']].dropna()

    # Label based on star_rating
    df['sentiment'] = df['star_rating'].apply(lambda x:
        'positive' if x >= 4.0 else
        'neutral' if x >= 3.0 else
        'negative'
    )

    print(f"\nDataset Statistics:")
    print(f"Total samples: {len(df)}")
    print(f"Sentiment distribution:")
    print(df['sentiment'].value_counts())
    print(f"\nStar rating distribution:")
    print(df['star_rating'].value_counts().sort_index())

    return df['comments'].tolist(), df['sentiment'].tolist()

def preprocess_text(text_list):
    """
    Text preprocessing:
    - Lowercase
    - Remove special characters
    - Tokenization (implicit in TF-IDF)
    - Remove stopwords
    - Lemmatization
    """
    # Download required NLTK data
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    processed = []
    for i, text in enumerate(text_list):
        if i % 1000 == 0:
            print(f"  Processing {i}/{len(text_list)}...")

        # Lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize and remove stopwords
        words = [lemmatizer.lemmatize(word) for word in text.split()
                 if word not in stop_words and len(word) > 2]
        processed.append(' '.join(words))

    return processed

def train_sentiment_model():
    """Train sentiment classification model"""
    print("=" * 60)
    print("SENTIMENT CLASSIFICATION MODEL TRAINING")
    print("=" * 60)

    print("\n[1/5] Loading data...")
    X_raw, y = load_and_prepare_data()

    print("\n[2/5] Preprocessing text...")
    X = preprocess_text(X_raw)

    print("\n[3/5] Vectorizing...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_vec = vectorizer.fit_transform(X)
    print(f"  Feature shape: {X_vec.shape}")

    print("\n[4/5] Splitting and training data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train samples: {X_train.shape[0]}")
    print(f"  Test samples: {X_test.shape[0]}")

    print("\n  Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, multi_class='ovr', random_state=42)
    model.fit(X_train, y_train)

    print("\n[5/5] Evaluating model...")
    y_pred = model.predict(X_test)
    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(classification_report(y_test, y_pred))

    print("\n" + "=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)
    cm = confusion_matrix(y_test, y_pred)
    print("              Predicted")
    print("             Neg Neu Pos")
    labels = ['negative', 'neutral', 'positive']
    for i, label in enumerate(labels):
        print(f"Actual {label:8s} {cm[i]}")

    # Calculate overall accuracy
    accuracy = (y_pred == y_test).mean()
    print(f"\nOverall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # Save models
    print("\n" + "=" * 60)
    print("Saving models...")
    print("=" * 60)
    joblib.dump(vectorizer, 'models/vectorizer.pkl')
    print("  ✓ Saved: models/vectorizer.pkl")

    joblib.dump(model, 'models/sentiment_model.pkl')
    print("  ✓ Saved: models/sentiment_model.pkl")

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Models saved to models/ directory")
    print(f"Final accuracy: {accuracy*100:.2f}%")

if __name__ == "__main__":
    train_sentiment_model()
