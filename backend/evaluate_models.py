import joblib
import pandas as pd
import os
from train_sentiment import preprocess_text

def load_models():
    """Load all trained models"""
    print("Loading trained models...")

    if not os.path.exists('models/vectorizer.pkl'):
        raise FileNotFoundError("vectorizer.pkl not found! Run train_all.py first.")
    if not os.path.exists('models/sentiment_model.pkl'):
        raise FileNotFoundError("sentiment_model.pkl not found! Run train_all.py first.")
    if not os.path.exists('models/category_model.pkl'):
        raise FileNotFoundError("category_model.pkl not found! Run train_all.py first.")
    if not os.path.exists('models/mlb.pkl'):
        raise FileNotFoundError("mlb.pkl not found! Run train_all.py first.")

    vectorizer = joblib.load('models/vectorizer.pkl')
    sentiment_model = joblib.load('models/sentiment_model.pkl')
    category_model = joblib.load('models/category_model.pkl')
    mlb = joblib.load('models/mlb.pkl')

    print("  ✓ All models loaded successfully\n")
    return vectorizer, sentiment_model, category_model, mlb

def test_predictions(test_comments):
    """Test models with sample comments"""
    vectorizer, sentiment_model, category_model, mlb = load_models()

    print("Processing test comments...")
    processed = preprocess_text(test_comments)
    X = vectorizer.transform(processed)

    # Predict
    sentiments = sentiment_model.predict(X)
    categories = mlb.inverse_transform(category_model.predict(X))

    # Get probabilities for sentiment
    sentiment_probs = sentiment_model.predict_proba(X)

    # Display results
    print("\n" + "=" * 80)
    print(" " * 25 + "PREDICTION RESULTS")
    print("=" * 80)

    for i, (comment, sentiment, cats) in enumerate(zip(test_comments, sentiments, categories), 1):
        print(f"\n[Test {i}]")
        print(f"Comment: {comment[:100]}{'...' if len(comment) > 100 else ''}")
        print(f"────────────────────────────────────────────────────────────────────────────────────")
        print(f"Sentiment: {sentiment.upper()}")

        # Show probability distribution
        probs = sentiment_probs[i]
        print(f"Confidence: Negative={probs[0]:.2%}, Neutral={probs[1]:.2%}, Positive={probs[2]:.2%}")

        print(f"Categories: {', '.join(cats) if len(cats) > 0 else 'None detected'}")

    print("\n" + "=" * 80)

    # Summary statistics
    sentiment_counts = pd.Series(sentiments).value_counts()
    print("\nSUMMARY STATISTICS")
    print("────────────────────────────────────────────────────────────────────────────────────")
    print(f"Total comments tested: {len(test_comments)}")
    print(f"\nSentiment Distribution:")
    for sent, count in sentiment_counts.items():
        print(f"  {sent.capitalize()}: {count}")

    # Flatten all categories
    all_cats = []
    for cats in categories:
        all_cats.extend(cats)
    if all_cats:
        cat_counts = pd.Series(all_cats).value_counts()
        print(f"\nCategory Distribution:")
        for cat, count in cat_counts.items():
            print(f"  {cat}: {count}")

    print("=" * 80)

# Sample test cases
TEST_COMMENTS = [
    "The professor explains concepts very clearly and makes difficult topics easy to understand. Great lecturer!",
    "He speaks too fast and rushes through the material, hard to follow. Can't keep up with the pace.",
    "Great course! Well organized and structured. The syllabus was clear from the beginning.",
    "Very unresponsive to emails and doesn't answer questions during office hours. Hard to reach.",
    "Fair grading and respectful to all students. Very professional and approachable.",
    "I don't have much to say, it was okay. Nothing special but nothing terrible either.",
    "Confusing lectures, unclear explanations, and the course structure is all over the place. Disorganized.",
    "Amazing professor! Caring, understanding, and always willing to help. Best class ever!",
    "Rude, arrogant, and unprofessional. Makes students feel stupid for asking questions.",
    "Clear voice, appropriate pace, and well organized materials. Easy to learn from this instructor."
]

def interactive_mode():
    """Interactive mode for testing custom comments"""
    print("\n" + "=" * 80)
    print(" " * 25 + "INTERACTIVE MODE")
    print("=" * 80)
    print("Enter your own comments to analyze (or 'quit' to exit)\n")

    vectorizer, sentiment_model, category_model, mlb = load_models()

    while True:
        comment = input("\nEnter a comment: ").strip()

        if comment.lower() in ['quit', 'exit', 'q']:
            print("Exiting interactive mode...")
            break

        if not comment:
            continue

        # Process and predict
        processed = preprocess_text([comment])
        X = vectorizer.transform(processed)

        sentiment = sentiment_model.predict(X)[0]
        probs = sentiment_model.predict_proba(X)[0]
        categories = mlb.inverse_transform(category_model.predict(X))[0]

        print(f"\n─" * 40)
        print(f"Sentiment: {sentiment.upper()}")
        print(f"Confidence: Negative={probs[0]:.2%}, Neutral={probs[1]:.2%}, Positive={probs[2]:.2%}")
        print(f"Categories: {', '.join(categories) if len(categories) > 0 else 'None detected'}")
        print("─" * 40)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ['-i', '--interactive']:
        interactive_mode()
    else:
        print("=" * 80)
        print(" " * 20 + "NLP MODEL EVALUATION & TESTING")
        print("=" * 80)
        print("\nRunning with default test cases...")
        print("Use '-i' or '--interactive' flag for interactive mode.\n")

        test_predictions(TEST_COMMENTS)

        print("\n" + "=" * 80)
        print("To test your own comments, run:")
        print("  python evaluate_models.py -i")
        print("=" * 80)
