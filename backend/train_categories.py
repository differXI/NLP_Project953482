import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, hamming_loss
import joblib
import os

# Category keywords dictionaries
CATEGORY_KEYWORDS = {
    'teaching_clarity': {
        'positive': ['clear', 'understandable', 'well explained', 'easy to follow',
                     'explains well', 'makes sense', 'thorough explanation',
                     'great explanation', 'very clear', 'easy to understand'],
        'negative': ['confusing', 'unclear', 'hard to follow', 'doesnt explain',
                     'difficult to understand', 'unclear explanation', 'confusing',
                     'not clear', 'hard to understand', 'poor explanation']
    },
    'speaking_pace': {
        'positive': ['clear voice', 'good pace', 'appropriate speed', 'easy to hear',
                     'speaks clearly', 'good speaker', 'well spoken'],
        'negative': ['too fast', 'rushes', 'too slow', 'mumbles', 'hard to hear',
                     'speaks too fast', 'rushed', 'dragged on', 'monotone',
                     'boring', 'hard to hear']
    },
    'course_structure': {
        'positive': ['organized', 'structured', 'well planned', 'clear syllabus',
                     'good organization', 'well organized course', 'organized course',
                     'well structured', 'great structure'],
        'negative': ['disorganized', 'unstructured', 'messy', 'no structure',
                     'poorly organized', 'confusing structure', 'all over the place',
                     'no organization']
    },
    'communication': {
        'positive': ['helpful', 'responsive', 'answers questions', 'accessible',
                     'available', 'great communication', 'quick to respond',
                     'always available', 'easy to reach', 'open door policy'],
        'negative': ['unresponsive', 'doesnt answer', 'ignores questions',
                     'hard to reach', 'unavailable', 'poor communication',
                     'never available', 'no response', 'hard to contact']
    },
    'professional_behavior': {
        'positive': ['professional', 'respectful', 'fair', 'caring', 'understanding',
                     'nice', 'kind', 'approachable', 'friendly'],
        'negative': ['rude', 'unprofessional', 'unfair', 'disrespectful',
                     'biased', 'unfair grading', 'arrogant', 'condescending']
    }
}

def create_category_labels(comments):
    """
    สร้าง labels สำหรับ categories โดยใช้ keyword matching

    Returns:
        List of sets แต่ละ set มี categories ที่เกี่ยวข้องกับ comment
    """
    labels = []

    for i, comment in enumerate(comments):
        if i % 1000 == 0:
            print(f"  Labeling {i}/{len(comments)}...")

        comment_lower = comment.lower()
        comment_categories = set()

        for category, keywords in CATEGORY_KEYWORDS.items():
            # Check if any keyword (positive or negative) appears in comment
            all_keywords = keywords['positive'] + keywords['negative']
            if any(keyword in comment_lower for keyword in all_keywords):
                comment_categories.add(category)

        labels.append(comment_categories)

    return labels

def preprocess_text(text_list):
    """
    Text preprocessing - ใช้ logic เดียวกับ train_sentiment
    """
    from train_sentiment import preprocess_text
    return preprocess_text(text_list)

def train_category_model():
    """Train multi-label category classification model"""
    print("=" * 60)
    print("MULTI-LABEL CATEGORY CLASSIFICATION MODEL TRAINING")
    print("=" * 60)

    print("\n[1/6] Loading data...")
    df = pd.read_csv("data/RateMyProfessor_Sample.csv")
    df = df[['comments']].dropna()

    comments = df['comments'].tolist()
    print(f"  Total comments: {len(comments)}")

    print("\n[2/6] Creating labels from keywords...")
    y_raw = create_category_labels(comments)

    # Count labels
    label_counts = {}
    for labels in y_raw:
        for label in labels:
            label_counts[label] = label_counts.get(label, 0) + 1

    print(f"\n  Category label distribution:")
    for cat, count in sorted(label_counts.items()):
        print(f"    {cat}: {count}")

    # Count samples with multiple labels
    multi_label_count = sum(1 for labels in y_raw if len(labels) > 1)
    no_label_count = sum(1 for labels in y_raw if len(labels) == 0)

    print(f"\n  Samples with multiple labels: {multi_label_count}")
    print(f"  Samples with no labels: {no_label_count}")

    # Filter out comments with no labels
    print("\n[3/6] Filtering samples without labels...")
    valid_indices = [i for i, labels in enumerate(y_raw) if len(labels) > 0]
    comments = [comments[i] for i in valid_indices]
    y_raw = [y_raw[i] for i in valid_indices]

    print(f"  Training samples after filtering: {len(comments)}")

    print("\n[4/6] Preprocessing and vectorizing...")
    # Load vectorizer from sentiment training (use same features)
    if not os.path.exists('models/vectorizer.pkl'):
        raise FileNotFoundError("vectorizer.pkl not found! Run train_sentiment.py first.")

    vectorizer = joblib.load('models/vectorizer.pkl')
    print("  Loaded existing vectorizer from models/vectorizer.pkl")

    X = preprocess_text(comments)
    X_vec = vectorizer.transform(X)
    print(f"  Feature shape: {X_vec.shape}")

    # Binarize labels
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(y_raw)

    print(f"\n  Categories: {list(mlb.classes_)}")
    print(f"  Label matrix shape: {y.shape}")

    print("\n[5/6] Splitting and training data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42
    )
    print(f"  Train samples: {X_train.shape[0]}")
    print(f"  Test samples: {X_test.shape[0]}")

    print("\n  Training OneVsRest Logistic Regression model...")
    model = OneVsRestClassifier(LogisticRegression(max_iter=1000, random_state=42))
    model.fit(X_train, y_train)

    print("\n[6/6] Evaluating model...")
    y_pred = model.predict(X_test)

    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT (Per Category)")
    print("=" * 60)
    print(classification_report(y_test, y_pred, target_names=mlb.classes_, zero_division=0))

    # Calculate Hamming loss (fraction of labels that are incorrectly predicted)
    h_loss = hamming_loss(y_test, y_pred)
    print(f"\nHamming Loss: {h_loss:.4f} (lower is better)")

    # Calculate per-category accuracy
    print("\nPer-Category Accuracy:")
    for i, cat in enumerate(mlb.classes_):
        cat_acc = (y_test[:, i] == y_pred[:, i]).mean()
        print(f"  {cat}: {cat_acc:.4f} ({cat_acc*100:.2f}%)")

    # Save models
    print("\n" + "=" * 60)
    print("Saving models...")
    print("=" * 60)
    joblib.dump(model, 'models/category_model.pkl')
    print("  ✓ Saved: models/category_model.pkl")

    joblib.dump(mlb, 'models/mlb.pkl')
    print("  ✓ Saved: models/mlb.pkl")

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Models saved to models/ directory")
    print(f"Number of categories: {len(mlb.classes_)}")

if __name__ == "__main__":
    train_category_model()
