"""
Multi-Label Category Classification Training Script

Trains a classifier to categorize professor comments into 5 categories:
1. Teaching Clarity
2. Speaking Pace
3. Course Structure
4. Communication
5. Professional Behavior

Uses keyword-based labeling to create training data.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import classification_report, hamming_loss
import joblib
import os

# Category keywords dictionary for labeling
CATEGORY_KEYWORDS = {
    'teaching_clarity': {
        'positive': [
            'clear', 'understandable', 'well explained', 'easy to follow',
            'explains well', 'makes sense', 'thorough explanation',
            'great explanation', 'very clear', 'easy to understand',
            'explains concepts', 'good explanations', 'understand',
            'clarity', 'articulate', 'well organized lectures'
        ],
        'negative': [
            'confusing', 'unclear', 'hard to follow', 'doesnt explain',
            'difficult to understand', 'unclear explanation', 'confusing lectures',
            'rambles', 'unclear teaching', 'hard to grasp',
            'lacks clarity', 'unclear instructions', 'confusing'
        ]
    },
    'speaking_pace': {
        'positive': [
            'clear voice', 'good pace', 'appropriate pace', 'easy to hear',
            'speaks clearly', 'good speaker', 'pleasant voice', 'well spoken',
            'articulate', 'clear speech', 'right pace', 'modulates voice'
        ],
        'negative': [
            'too fast', 'rushes', 'rushed', 'too slow', 'mumbles',
            'hard to hear', 'speaks too fast', 'rushed through',
            'speaks fast', 'slow speaker', 'monotone', 'hard to understand speech',
            'mumbling', 'talks too fast', 'rushed through material'
        ]
    },
    'course_structure': {
        'positive': [
            'organized', 'structured', 'well planned', 'clear syllabus',
            'good organization', 'well organized', 'structured course',
            'well laid out', 'good structure', 'organized class',
            'clear structure', 'well designed', 'logical flow'
        ],
        'negative': [
            'disorganized', 'unstructured', 'messy', 'no structure',
            'poorly organized', 'lacks structure', 'disorganized class',
            'unorganized course', 'all over the place', 'no clear structure',
            'chaotic', 'disorganized lectures', 'poor organization'
        ]
    },
    'communication': {
        'positive': [
            'helpful', 'responsive', 'answers questions', 'accessible',
            'available', 'great communication', 'quick to respond',
            'always available', 'open door', 'approachable', 'willing to help',
            'responsive to questions', 'helpful outside class'
        ],
        'negative': [
            'unresponsive', 'doesnt answer', 'ignores questions',
            'hard to reach', 'unavailable', 'poor communication',
            'never available', 'ignores students', 'doesnt respond',
            'unresponsive to emails', 'inaccessible', 'not helpful'
        ]
    },
    'professional_behavior': {
        'positive': [
            'professional', 'respectful', 'fair', 'caring', 'understanding',
            'kind', 'patient', 'supportive', 'reasonable', 'ethical',
            'fair grading', 'treats students with respect', 'approachable'
        ],
        'negative': [
            'rude', 'unprofessional', 'unfair', 'disrespectful',
            'biased', 'unfair grading', 'arrogant', 'condescending',
            'unfair to students', 'rude to students', 'unprofessional behavior',
            'belittles students', 'inappropriate'
        ]
    }
}


def create_category_labels(comments):
    """
    Create labels for categories using keyword matching

    Args:
        comments: List of comment strings

    Returns:
        List of sets containing category labels for each comment
    """
    print("Creating category labels using keyword matching...")

    labels = []
    category_counts = {cat: 0 for cat in CATEGORY_KEYWORDS.keys()}
    no_match_count = 0

    for i, comment in enumerate(comments):
        if i % 10000 == 0:
            print(f"  Processing {i}/{len(comments)}...")

        comment_lower = str(comment).lower()
        comment_categories = set()

        # Check each category
        for category, keywords in CATEGORY_KEYWORDS.items():
            # Check if any keyword appears in comment
            all_keywords = keywords['positive'] + keywords['negative']
            if any(keyword in comment_lower for keyword in all_keywords):
                comment_categories.add(category)
                category_counts[category] += 1

        # If no category matched, this is okay (multi-label can have empty set)
        if len(comment_categories) == 0:
            no_match_count += 1

        labels.append(comment_categories)

    print(f"\n  Category Distribution:")
    for cat, count in category_counts.items():
        percentage = (count / len(comments)) * 100
        print(f"    {cat}: {count} ({percentage:.1f}%)")
    print(f"    No category matched: {no_match_count} ({(no_match_count/len(comments)*100):.1f}%)")

    return labels


def load_vectorizer(vectorizer_path="models/vectorizer.pkl"):
    """Load existing vectorizer or create new one"""
    if os.path.exists(vectorizer_path):
        print(f"Loading existing vectorizer from {vectorizer_path}...")
        return joblib.load(vectorizer_path)
    else:
        print("Vectorizer not found. Please train sentiment model first!")
        raise FileNotFoundError(f"{vectorizer_path} not found. Run train_sentiment.py first.")


def preprocess_with_vectorizer(comments, vectorizer):
    """Preprocess comments using existing vectorizer"""
    # The vectorizer already handles preprocessing
    # Just need to clean the text a bit
    import re

    processed = []
    for comment in comments:
        # Basic cleaning
        text = str(comment).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        processed.append(text)

    # Transform using vectorizer
    return vectorizer.transform(processed)


def train_category_model(data_path="data/RateMyProfessor_Sample.csv",
                          model_dir="models",
                          test_size=0.2):
    """
    Train multi-label category classification model

    Args:
        data_path: Path to the CSV dataset
        model_dir: Directory to save/load models
        test_size: Proportion of data for testing

    Returns:
        Dictionary containing model performance metrics
    """
    print("\n" + "="*60)
    print("MULTI-LABEL CATEGORY CLASSIFICATION MODEL TRAINING")
    print("="*60)

    # Create model directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)

    # 1. Load data
    print(f"\nLoading data from {data_path}...")
    df = pd.read_csv(data_path)

    if 'comments' not in df.columns:
        raise ValueError("Column 'comments' not found in dataset")

    df = df[['comments']].dropna()
    comments = df['comments'].tolist()

    print(f"  Loaded {len(comments)} comments")

    # 2. Create labels
    y_raw = create_category_labels(comments)

    # Filter out comments with no labels (optional - can keep them too)
    valid_indices = [i for i, labels in enumerate(y_raw) if len(labels) > 0]

    if len(valid_indices) < len(comments) * 0.5:
        print(f"\n  WARNING: Only {len(valid_indices)}/{len(comments)} comments have labels")
        print("  This might result in poor model performance")

    # Use only comments with labels for training
    comments_filtered = [comments[i] for i in valid_indices]
    y_raw_filtered = [y_raw[i] for i in valid_indices]

    print(f"\n  Using {len(comments_filtered)} labeled comments for training")

    # 3. Load or create vectorizer
    vectorizer = load_vectorizer(os.path.join(model_dir, 'vectorizer.pkl'))

    # 4. Preprocess and vectorize
    print("\nVectorizing comments...")
    X = preprocess_with_vectorizer(comments_filtered, vectorizer)
    print(f"  Feature matrix shape: {X.shape}")

    # 5. Binarize labels
    print("\nBinarizing labels...")
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(y_raw_filtered)

    print(f"  Classes: {mlb.classes_}")
    print(f"  Label matrix shape: {y.shape}")

    # 6. Split data
    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    print(f"  Training set: {len(X_train)} samples")
    print(f"  Test set: {len(X_test)} samples")

    # 7. Train model
    print("\nTraining OneVsRestClassifier with LogisticRegression...")
    model = OneVsRestClassifier(
        LogisticRegression(max_iter=1000, random_state=42),
        n_jobs=-1  # Use all CPU cores
    )
    model.fit(X_train, y_train)
    print("  Training complete!")

    # 8. Evaluate
    print("\n" + "-"*60)
    print("MODEL EVALUATION")
    print("-"*60)

    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Calculate accuracy
    train_accuracy = (y_train_pred == y_train).mean()
    test_accuracy = (y_test_pred == y_test).mean()

    print(f"\nTraining Exact Match Accuracy: {train_accuracy:.4f}")
    print(f"Test Exact Match Accuracy: {test_accuracy:.4f}")

    # Hamming loss (fraction of labels that are incorrectly predicted)
    train_hamming = hamming_loss(y_train, y_train_pred)
    test_hamming = hamming_loss(y_test, y_test_pred)

    print(f"\nTraining Hamming Loss: {train_hamming:.4f}")
    print(f"Test Hamming Loss: {test_hamming:.4f}")

    # Classification report for each category
    print("\nPer-Category Classification Report:")
    print(classification_report(y_test, y_test_pred, target_names=mlb.classes_))

    # 9. Save models
    print("\n" + "-"*60)
    print("SAVING MODELS")
    print("-"*60)

    category_model_path = os.path.join(model_dir, 'category_model.pkl')
    mlb_path = os.path.join(model_dir, 'mlb.pkl')

    joblib.dump(model, category_model_path)
    print(f"  ✓ Model saved to {category_model_path}")

    joblib.dump(mlb, mlb_path)
    print(f"  ✓ MultiLabelBinarizer saved to {mlb_path}")

    # 10. Display statistics
    print("\n" + "-"*60)
    print("LABEL STATISTICS")
    print("-"*60)

    for i, category in enumerate(mlb.classes_):
        train_count = y_train[:, i].sum()
        test_count = y_test[:, i].sum()
        print(f"\n{category}:")
        print(f"  Training samples: {int(train_count)}")
        print(f"  Test samples: {int(test_count)}")

    # Return metrics
    metrics = {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'train_hamming_loss': train_hamming,
        'test_hamming_loss': test_hamming,
        'classification_report': classification_report(y_test, y_test_pred, target_names=mlb.classes_, output_dict=True),
        'classes': mlb.classes_.tolist(),
        'num_samples': len(comments_filtered)
    }

    return metrics


if __name__ == "__main__":
    import sys

    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/RateMyProfessor_Sample.csv"

    try:
        metrics = train_category_model(data_path=data_path)

        print("\n" + "="*60)
        print("TRAINING COMPLETE!")
        print("="*60)
        print(f"Test Accuracy: {metrics['test_accuracy']:.4f}")
        print(f"Test Hamming Loss: {metrics['test_hamming_loss']:.4f}")
        print(f"Categories: {metrics['classes']}")
        print(f"Samples Used: {metrics['num_samples']}")
        print("="*60)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
