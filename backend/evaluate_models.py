"""
NLP Model Evaluation and Testing Script

Test trained sentiment and category models with sample comments.
Supports both batch testing and interactive mode.
"""

import joblib
import pandas as pd
import os
import sys


def load_models():
    """Load all trained models"""
    print("Loading trained models...")

    # Check if model files exist
    required_files = {
        'vectorizer.pkl': 'TF-IDF Vectorizer',
        'sentiment_model.pkl': 'Sentiment Classifier',
        'category_model.pkl': 'Category Classifier',
        'mlb.pkl': 'MultiLabelBinarizer'
    }

    model_dir = 'models'
    missing_files = []

    for filename, description in required_files.items():
        filepath = os.path.join(model_dir, filename)
        if not os.path.exists(filepath):
            missing_files.append(filename)
            print(f"  ✗ {description} not found")
        else:
            print(f"  ✓ {description} loaded")

    if missing_files:
        print(f"\nERROR: Missing model files: {', '.join(missing_files)}")
        print("Please run 'python train_all.py' first to train the models.")
        sys.exit(1)

    # Load models
    vectorizer = joblib.load(os.path.join(model_dir, 'vectorizer.pkl'))
    sentiment_model = joblib.load(os.path.join(model_dir, 'sentiment_model.pkl'))
    category_model = joblib.load(os.path.join(model_dir, 'category_model.pkl'))
    mlb = joblib.load(os.path.join(model_dir, 'mlb.pkl'))

    print("\n✓ All models loaded successfully\n")

    return vectorizer, sentiment_model, category_model, mlb


def preprocess_text(text_list, vectorizer):
    """Preprocess text using the vectorizer"""
    import re

    processed = []
    for text in text_list:
        # Basic cleaning
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        processed.append(text)

    # Transform using vectorizer
    return vectorizer.transform(processed)


def test_predictions(test_comments, vectorizer, sentiment_model, category_model, mlb):
    """Test models with sample comments"""
    print("Processing test comments...")

    # Preprocess
    processed = preprocess_text(test_comments, vectorizer)
    X = vectorizer.transform(processed)

    # Predict sentiment
    sentiments = sentiment_model.predict(X)
    sentiment_probs = sentiment_model.predict_proba(X)

    # Predict categories
    categories = mlb.inverse_transform(category_model.predict(X))

    # Display results
    print("\n" + "="*80)
    print(" " * 25 + "PREDICTION RESULTS")
    print("="*80)

    for i, (comment, sentiment, cats) in enumerate(zip(test_comments, sentiments, categories), 1):
        # Truncate long comments for display
        display_comment = comment[:100] + '...' if len(comment) > 100 else comment

        print(f"\n[Test {i}]")
        print(f"Comment: {display_comment}")
        print(f"{'─'*80}")

        # Sentiment with confidence
        print(f"Sentiment: {sentiment.upper()}")
        probs = sentiment_probs[i]
        print(f"Confidence: Negative={probs[0]:.2%}, Neutral={probs[1]:.2%}, Positive={probs[2]:.2%}")

        # Categories
        if len(cats) > 0:
            print(f"Categories: {', '.join(cats)}")
        else:
            print(f"Categories: None detected")

    # Summary statistics
    sentiment_counts = pd.Series(sentiments).value_counts()
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Total comments tested: {len(test_comments)}")
    print(f"\nSentiment Distribution:")
    for sent in ['negative', 'neutral', 'positive']:
        count = sentiment_counts.get(sent, 0)
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
    else:
        print("\nNo categories detected in any comments.")

    print("="*80)


def interactive_mode(vectorizer, sentiment_model, category_model, mlb):
    """Interactive mode for testing custom comments"""
    print("\n" + "="*80)
    print(" " * 30 + "INTERACTIVE MODE")
    print("="*80)
    print("\nEnter your own comments to analyze")
    print("Commands: 'quit' or 'exit' to quit, 'clear' to clear screen\n")

    comment_count = 0

    while True:
        try:
            comment = input("\nEnter a comment: ").strip()

            if comment.lower() in ['quit', 'exit', 'q']:
                print("\nExiting interactive mode...")
                break

            if comment.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue

            if not comment:
                continue

            comment_count += 1

            # Process and predict
            processed = preprocess_text([comment], vectorizer)
            X = vectorizer.transform(processed)

            sentiment = sentiment_model.predict(X)[0]
            probs = sentiment_model.predict_proba(X)[0]
            categories = mlb.inverse_transform(category_model.predict(X))[0]

            # Display result
            print(f"\n{'─'*40}")
            print(f"Comment #{comment_count}")
            print(f"{'─'*40}")
            print(f"Sentiment: {sentiment.upper()}")
            print(f"Confidence: Negative={probs[0]:.2%}, Neutral={probs[1]:.2%}, Positive={probs[2]:.2%}")

            if len(categories) > 0:
                print(f"Categories: {', '.join(categories)}")
            else:
                print(f"Categories: None detected")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            continue


def evaluate_on_dataset(data_path="data/RateMyProfessor_Sample.csv", sample_size=100):
    """Evaluate models on a sample from the dataset"""
    print(f"\nEvaluating on sample from {data_path}...")

    # Load data
    df = pd.read_csv(data_path)
    df = df[['comments']].dropna()

    # Sample
    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42)

    comments = df['comments'].tolist()

    # Load models
    vectorizer, sentiment_model, category_model, mlb = load_models()

    # Test
    test_predictions(comments, vectorizer, sentiment_model, category_model, mlb)


# Sample test cases
TEST_COMMENTS = [
    "The professor explains concepts very clearly and makes difficult topics easy to understand.",
    "He speaks too fast and rushes through the material, very hard to follow.",
    "Great course! Well organized and structured. The syllabus was clear from the beginning.",
    "Very unresponsive to emails and doesn't answer questions during office hours.",
    "Fair grading and respectful to all students. Very professional and approachable.",
    "I don't have much to say, it was okay. Nothing special but nothing terrible either.",
    "Confusing lectures, unclear explanations, and the course structure is all over the place.",
    "Amazing professor! Caring, understanding, and always willing to help. Best class ever!",
    "Rude, arrogant, and unprofessional. Makes students feel stupid for asking questions.",
    "Clear voice, appropriate pace, and well organized materials. Easy to learn from this instructor.",
    "The teaching is confusing and the professor is unresponsive to student questions.",
    "Well-structured course with great communication. The instructor is always available to help."
]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Evaluate NLP models')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Run in interactive mode')
    parser.add_argument('-d', '--dataset', action='store_true',
                        help='Evaluate on dataset sample')
    parser.add_argument('-s', '--sample-size', type=int, default=100,
                        help='Sample size for dataset evaluation (default: 100)')

    args = parser.parse_args()

    if args.interactive:
        # Interactive mode
        vectorizer, sentiment_model, category_model, mlb = load_models()
        interactive_mode(vectorizer, sentiment_model, category_model, mlb)
    elif args.dataset:
        # Dataset evaluation
        evaluate_on_dataset(sample_size=args.sample_size)
    else:
        # Default: run with test cases
        print("="*80)
        print(" " * 20 + "NLP MODEL EVALUATION")
        print("="*80)
        print("\nRunning with default test cases...")
        print("Options:")
        print("  -i, --interactive    Run in interactive mode")
        print("  -d, --dataset       Evaluate on dataset sample")
        print("  -s, --sample-size N  Sample size for dataset evaluation\n")

        # Load models and test
        vectorizer, sentiment_model, category_model, mlb = load_models()
        test_predictions(TEST_COMMENTS, vectorizer, sentiment_model, category_model, mlb)

        print("\n" + "="*80)
        print("To test your own comments, run:")
        print("  python evaluate_models.py -i")
        print("="*80)
