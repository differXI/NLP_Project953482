"""
NLP Model Evaluation and Testing Script

Test trained sentiment and category models with sample comments.
Supports both batch testing and interactive mode.
"""

import joblib
import pandas as pd
import os
import sys
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from analytics import analyze_text

def setup_nltk():
    try:
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading NLTK data...")
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)

def load_models():
    """Load all trained models"""
    print("Loading trained models...")

    # อัปเดตให้โหลด Vectorizer 2 ตัว (แยกกัน)
    required_files = {
        'vectorizer.pkl': 'Sentiment TF-IDF Vectorizer',
        'sentiment_model.pkl': 'Sentiment Classifier',
        'category_vectorizer.pkl': 'Category TF-IDF Vectorizer',
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
    sent_vec = joblib.load(os.path.join(model_dir, 'vectorizer.pkl'))
    sent_model = joblib.load(os.path.join(model_dir, 'sentiment_model.pkl'))
    cat_vec = joblib.load(os.path.join(model_dir, 'category_vectorizer.pkl'))
    cat_model = joblib.load(os.path.join(model_dir, 'category_model.pkl'))
    mlb = joblib.load(os.path.join(model_dir, 'mlb.pkl'))

    print("\n✓ All models loaded successfully\n")

    return sent_vec, sent_model, cat_vec, cat_model, mlb


def preprocess_text(text_list):
    """ทำความสะอาดข้อความด้วย Lemmatization ให้ตรงกับตอนเทรนเป๊ะๆ"""
    setup_nltk()
    stop_words = set(stopwords.words('english'))
    negation_words = {"not", "no", "nor", "doesn't", "isn't", "didn't", "wasn't", "wouldn't", "can't", "cannot", "couldn't", "won't"}
    stop_words = stop_words - negation_words
    
    lemmatizer = WordNetLemmatizer()
    processed = []

    for text in text_list:
        text = str(text).lower()
        text = text.replace('-', ' ')
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        words = [
            lemmatizer.lemmatize(word) for word in text.split() 
            if word not in stop_words and len(word) > 2
        ]
        processed.append(' '.join(words))

    return processed


def test_predictions(test_comments):
    print("Processing test comments...")
    print("\n" + "="*80)
    print(" " * 25 + "PREDICTION RESULTS")
    print("="*80)

    sentiments_list = []
    all_cats = [] # ประกาศตัวแปรเก็บ Category รวมไว้ตรงนี้เลย
    
    for i, comment in enumerate(test_comments, 1):
        display_comment = comment[:100] + '...' if len(comment) > 100 else comment
        
        # เรียกใช้ฟังก์ชันเดียวจบ
        sentiment, cats, confidence = analyze_text(comment)
        
        # เก็บค่าสะสมไว้ทำ Summary ตอนท้าย
        sentiments_list.append(sentiment)
        all_cats.extend(cats) # เอา category ของคอมเมนต์นี้ไปต่อท้าย list รวม

        print(f"\n[Test {i}]")
        print(f"Comment: {display_comment}")
        print(f"{'─'*80}")
        print(f"Sentiment: {sentiment.upper()}")
        
        # ดึงเปอร์เซ็นต์มาโชว์
        conf_details = f"Negative={confidence['negative']:.2%}, Positive={confidence['positive']:.2%}"
        print(f"Confidence: {conf_details}")

        if len(cats) > 0:
            print(f"Categories: {', '.join(cats)}")
        else:
            print(f"Categories: None detected")

    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Total comments tested: {len(test_comments)}")
    
    print(f"\nSentiment Distribution:")
    sentiment_counts = pd.Series(sentiments_list).value_counts()
    for sent in sentiment_counts.index:
        print(f"  {sent.capitalize()}: {sentiment_counts[sent]}")

    # นับ Category จาก all_cats ที่เราเก็บสะสมมาได้เลย
    if all_cats:
        cat_counts = pd.Series(all_cats).value_counts()
        print(f"\nCategory Distribution:")
        for cat, count in cat_counts.items():
            print(f"  {cat}: {count}")
    else:
        print("\nNo categories detected in any comments.")
    print("="*80)


def interactive_mode(sent_vec, sent_model, cat_vec, cat_model, mlb):
    """Interactive mode for testing custom comments"""
    print("\n" + "="*80)
    print(" " * 30 + "INTERACTIVE MODE")
    print("="*80)
    print("\nEnter your own comments to analyze")
    print("Commands: 'quit' or 'exit' to quit, 'clear' to clear screen\n")

    comment_count = 0
    sent_classes = sent_model.classes_

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
            processed = preprocess_text([comment])
            X_sent = sent_vec.transform(processed)
            X_cat = cat_vec.transform(processed)

            sentiment = sent_model.predict(X_sent)[0]
            probs = sent_model.predict_proba(X_sent)[0]
            categories = mlb.inverse_transform(cat_model.predict(X_cat))[0]

            # Display result
            print(f"\n{'─'*40}")
            print(f"Comment #{comment_count}")
            print(f"{'─'*40}")
            print(f"Sentiment: {sentiment.upper()}")
            
            conf_details = ", ".join([f"{cls.capitalize()}={prob:.2%}" for cls, prob in zip(sent_classes, probs)])
            print(f"Confidence: {conf_details}")

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


def evaluate_on_dataset(data_path="./RateMyProfessor_Sample data.csv", sample_size=100):
    """Evaluate models on a sample from the dataset"""
    print(f"\nEvaluating on sample from {data_path}...")

    df = pd.read_csv(data_path)
    df = df[['comments']].dropna()

    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42)

    comments = df['comments'].tolist()
    sent_vec, sent_model, cat_vec, cat_model, mlb = load_models()
    test_predictions(comments, sent_vec, sent_model, cat_vec, cat_model, mlb)


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
    "Well-structured course with great communication. The instructor is always available to help.",
    "This class is pretty hard, but the professor is very supportive and provides helpful feedback on assignments.",
    "The lectures are boring. The materials are pretty disorganized and it's surprisingly hard to follow the course. I don't recommend this professor.",
    "She is an exelent talker and very clear in her explanations. But the grading is surprisingly harsh and the exam is pretty difficult. Her time management is quite bad, sometimes she starts the lecture very late and rushes through the materials at the end. Overall, I think she's a good professor but the course is quite challenging.",
    "U know wat, I really loveeeeeee this professor! 1ofa, he looks SO GOOD. He has a very clear voice and a charming smile;) that makes u want to pay attention in class.",
    "Ngl, this prof is lowkey a fever dream. Lectures r 10/10 borinng af & he talks sooooo fast u cant even take notes. But then he gives extra credit like its candy?? Sus but i guess i'll pass.",
    "Ajan is so jai-dee mak mak! Even though the exam was f*ing hard, he still helps us a lot. Best prof ever na krub, 10/10 recommended eiei.",
    "Oh, I just LOVE how the professor is SO CLEAR that I literally have no idea what's going on. Truly a masterpiece of confusion. 10/10 would recommend if u want to fail.",
    "This class is absolute INSANITY! The workload is BRUTAL and the exams are freaking KILLER, but man, you learn so much. Prof is a total BEAST in the best way possible. Best experience ever."
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
        sent_vec, sent_model, cat_vec, cat_model, mlb = load_models()
        interactive_mode(sent_vec, sent_model, cat_vec, cat_model, mlb)
    elif args.dataset:
        evaluate_on_dataset(sample_size=args.sample_size)
    else:
        print("="*80)
        print(" " * 20 + "NLP MODEL EVALUATION")
        print("="*80)
        print("\nRunning with default test cases...")
        print("Options:")
        print("  -i, --interactive    Run in interactive mode")
        print("  -d, --dataset       Evaluate on dataset sample")
        print("  -s, --sample-size N  Sample size for dataset evaluation\n")

        test_predictions(TEST_COMMENTS)

        print("\n" + "="*80)
        print("To test your own comments, run:")
        print("  python evaluate_models.py -i")
        print("="*80)