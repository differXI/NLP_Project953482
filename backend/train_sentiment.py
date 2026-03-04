"""
Sentiment Classification Training Script

Trains a Logistic Regression model to classify professor comments as:
- Positive (rating >= 4.0)
- Neutral (3.0 <= rating < 4.0)
- Negative (rating < 3.0)
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)


def load_and_prepare_data(data_path="data/RateMyProfessor_Sample.csv"):
    """
    Load comments and create sentiment labels based on star ratings

    Returns:
        X: list of comment texts
        y: list of sentiment labels
    """
    print(f"Loading data from {data_path}...")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")

    df = pd.read_csv(data_path)

    # Check required columns
    required_cols = ['star_rating', 'comments']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in dataset")

    # Drop rows with missing values
    df = df[['star_rating', 'comments']].dropna()

    print(f"  Loaded {len(df)} reviews")

    # Create sentiment labels based on star_rating
    df['sentiment'] = df['star_rating'].apply(lambda x:
        'positive' if x >= 4.0 else
        'neutral' if x >= 3.0 else
        'negative'
    )

    # Display label distribution
    print(f"\n  Label Distribution:")
    print(df['sentiment'].value_counts())
    print(f"  Percentage:")
    print(df['sentiment'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%')

    return df['comments'].tolist(), df['sentiment'].tolist()


def preprocess_text(text_list):
    """
    Text preprocessing for NLP

    Steps:
    1. Lowercase conversion
    2. Remove special characters and numbers
    3. Tokenization
    4. Stopword removal
    5. Lemmatization

    Args:
        text_list: List of text strings

    Returns:
        List of processed text strings
    """
    print("\nPreprocessing text...")

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    processed = []

    for i, text in enumerate(text_list):
        if i % 10000 == 0:
            print(f"  Processing {i}/{len(text_list)}...")

        # Convert to lowercase
        text = str(text).lower()

        # Remove special characters, numbers, and extra whitespace
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Tokenize and remove stopwords
        words = [lemmatizer.lemmatize(word) for word in text.split()
                 if word not in stop_words and len(word) > 2]

        processed.append(' '.join(words))

    print(f"  Preprocessed {len(processed)} texts")
    return processed


def train_sentiment_model(data_path="data/RateMyProfessor_Sample.csv",
                          model_dir="models",
                          test_size=0.2,
                          max_features=5000):
    """
    Train sentiment classification model

    Args:
        data_path: Path to the CSV dataset
        model_dir: Directory to save trained models
        test_size: Proportion of data for testing
        max_features: Maximum number of features for TF-IDF

    Returns:
        Dictionary containing model performance metrics
    """
    print("\n" + "="*60)
    print("SENTIMENT CLASSIFICATION MODEL TRAINING")
    print("="*60)

    # Create model directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)

    # 1. Load and prepare data
    X_raw, y = load_and_prepare_data(data_path)

    # 2. Preprocess text
    X = preprocess_text(X_raw)

    # 3. Vectorize using TF-IDF
    print("\nVectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),  # Use unigrams and bigrams
        min_df=2,  # Ignore terms that appear in less than 2 documents
        max_df=0.8  # Ignore terms that appear in more than 80% of documents
    )
    X_vec = vectorizer.fit_transform(X)

    print(f"  Feature matrix shape: {X_vec.shape}")
    print(f"  Vocabulary size: {len(vectorizer.vocabulary_)}")

    # 4. Split data
    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=test_size, random_state=42, stratify=y
    )
    print(f"  Training set: {len(X_train)} samples")
    print(f"  Test set: {len(X_test)} samples")

    # 5. Train model
    print("\nTraining Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        multi_class='multinomial',
        solver='lbfgs',
        random_state=42,
        class_weight='balanced'  # Handle class imbalance
    )
    model.fit(X_train, y_train)
    print("  Training complete!")

    # 6. Evaluate
    print("\n" + "-"*60)
    print("MODEL EVALUATION")
    print("-"*60)

    # Training accuracy
    train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, train_pred)
    print(f"\nTraining Accuracy: {train_accuracy:.4f}")

    # Test predictions
    y_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {test_accuracy:.4f}")

    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Negative', 'Neutral', 'Positive']))

    # Confusion matrix
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print("         Predicted")
    print("          Neg  Neu  Pos")
    labels = ['Neg', 'Neu', 'Pos']
    for i, label in enumerate(labels):
        print(f"Actual {label}: {cm[i]}")

    # 7. Save models
    print("\n" + "-"*60)
    print("SAVING MODELS")
    print("-"*60)

    vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
    model_path = os.path.join(model_dir, 'sentiment_model.pkl')

    joblib.dump(vectorizer, vectorizer_path)
    print(f"  ✓ Vectorizer saved to {vectorizer_path}")

    joblib.dump(model, model_path)
    print(f"  ✓ Model saved to {model_path}")

    # Get feature importance (top words for each class)
    print("\n" + "-"*60)
    print("FEATURE IMPORTANCE (Top words per class)")
    print("-"*60)

    feature_names = vectorizer.get_feature_names_out()
    class_labels = model.classes_

    for i, class_label in enumerate(class_labels):
        # Get coefficients for this class
        coef = model.coef_[i]

        # Get top 10 positive features
        top_indices = np.argsort(coef)[-10:][::-1]
        top_words = [feature_names[idx] for idx in top_indices]
        top_scores = [coef[idx] for idx in top_indices]

        print(f"\n{class_label.upper()}:")
        for word, score in zip(top_words, top_scores):
            print(f"  {word}: {score:.4f}")

    # Return performance metrics
    metrics = {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'classification_report': classification_report(y_test, y_pred, output_dict=True),
        'confusion_matrix': cm.tolist(),
        'feature_count': len(feature_names),
        'class_labels': class_labels.tolist()
    }

    return metrics


if __name__ == "__main__":
    import sys

    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/RateMyProfessor_Sample.csv"

    try:
        metrics = train_sentiment_model(data_path=data_path)

        print("\n" + "="*60)
        print("TRAINING COMPLETE!")
        print("="*60)
        print(f"Final Test Accuracy: {metrics['test_accuracy']:.4f}")
        print(f"Features: {metrics['feature_count']}")
        print(f"Classes: {metrics['class_labels']}")
        print("="*60)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
