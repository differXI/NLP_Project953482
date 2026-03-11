"""
Multi-Label Category Classification Training Script
- Uses Regex word-boundary matching to label training data.
- Builds its OWN TF-IDF Vectorizer (No more borrowing from Sentiment).
- Fixes Data Leakage by splitting before Vectorizing.
- Handles stopwords correctly (keeps negation words).
"""

import os
import re
import sys
import nltk
import joblib
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import classification_report, hamming_loss

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#  SETTINGS

CONFIG = {
    "data_path": os.path.join(BASE_DIR, "data", "RateMyProfessor_Sample.csv"),
    "model_dir": os.path.join(BASE_DIR, "models"),
    "test_size": 0.2,
    "max_features": 4000, # จำนวนคำศัพท์สูงสุดสำหรับหมวดหมู่
    "random_seed": 42
}

# พจนานุกรมคำศัพท์สำหรับแยกหมวดหมู่
CATEGORY_KEYWORDS = {
    'teaching_clarity': {
        'positive': [
            'clear', 'clearly', 'understand', 'well explained', 'easy to follow', 
            'explain well', 'make sense', 'thorough', 'great explanation', 
            'clarity', 'articulate', 'engaging', 'interesting', 'amazing lecture', 
            'good professor', 'great professor', 'excellent teacher', 'good lecture',
            'learn', 'teach', 'brilliant', 'smart', 'knowledgeable', 'material'
        ],
        'negative': [
            'confusing', 'unclear', 'hard to follow', 'doesnt explain', 'didnt explain',
            'difficult to understand', 'ramble', 'hard to grasp', 'lack clarity', 
            'boring', 'dry', 'read off slide', 'read from powerpoint', 'confused', 
            'terrible teacher', 'worst professor', 'heavy accent', 'cant understand'
        ]
    },
    'speaking_pace': {
        'positive': [
            'clear voice', 'good pace', 'appropriate pace', 'easy to hear', 
            'speak clearly', 'good speaker', 'pleasant voice', 'well spoken'
        ],
        'negative': [
            'too fast', 'rush', 'too slow', 'mumble', 'hard to hear', 
            'speak too fast', 'speak fast', 'monotone', 'quiet', 'soft spoken', 'cant hear'
        ]
    },
    'course_structure': {
        'positive': [
            'organized', 'structure', 'well planned', 'clear syllabus', 
            'logical flow', 'easy a', 'fair grading', 'clear grading criteria', 
            'extra credit', 'easy exam', 'fair test', 'easy class', 'straightforward', 'pass'
        ],
        'negative': [
            'disorganized', 'unstructured', 'messy', 'no structure', 'all over the place', 
            'chaotic', 'tough grader', 'test heavy', 'pop quiz', 'hard exam', 
            'harsh grader', 'too much work', 'heavy workload', 'difficult exam', 
            'hard test', 'unfair grading', 'fail'
        ],
        # เพิ่มหมวดกลางๆ เพราะพูดถึงเรื่องโครงสร้างวิชา
        'neutral': [
            'test', 'exam', 'homework', 'assignment', 'paper', 'quiz', 'project', 
            'book', 'textbook', 'study', 'grade', 'note', 'read'
        ]
    },
    'communication': {
        'positive': [
            'helpful', 'responsive', 'answer question', 'accessible', 'available', 
            'quick to respond', 'open door', 'approachable', 'willing to help', 
            'office hour', 'reply', 'email', 'accessible outside class', 'help', 'question'
        ],
        'negative': [
            'unresponsive', 'doesnt answer', 'ignore question', 'hard to reach', 
            'unavailable', 'poor communication', 'ignore student', 'doesnt respond', 
            'inaccessible', 'not helpful', 'never reply', 'ignore email', 'no response'
        ]
    },
    'professional_behavior': {
        'positive': [
            'professional', 'respectful', 'fair', 'caring', 'care',
            'kind', 'patient', 'supportive', 'reasonable', 'ethical', 'sweet', 'nice', 
            'funny', 'hilarious', 'inspirational', 'passionate', 'chill', 'accommodating',
            'awesome', 'fun', 'love', 'amazing', 'guy'
        ],
        'negative': [
            'rude', 'unprofessional', 'unfair', 'disrespectful', 'biased', 'arrogant', 
            'condescending', 'belittle', 'inappropriate', 'mean', 'strict', 
            'unreasonable', 'awful', 'terrible person', 'doesnt care', 'didnt care', 'bad', 'terrible'
        ]
    }
}


# 1. TEXT PREPARATION

def setup_nltk():
    try:
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading NLTK data...")
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)

def clean_text(texts):
    """ทำความสะอาดข้อความ โดยเก็บคำปฏิเสธ (not, no) เอาไว้"""
    print("Cleaning text... (This might take a moment)")
    stop_words = set(stopwords.words('english'))
    negation_words = {"not", "no", "nor", "doesn't", "isn't", "didn't", "wasn't", "wouldn't", "can't", "cannot", "couldn't", "won't"}
    stop_words = stop_words - negation_words
    
    lemmatizer = WordNetLemmatizer()
    processed = []

    for text in texts:
        text = text.replace('-', ' ')
        text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
        words = [
            lemmatizer.lemmatize(word) for word in text.split() 
            if word not in stop_words and len(word) > 2
        ]
        processed.append(' '.join(words))

    return processed

def create_category_labels(comments):
    """สร้าง Label ด้วย Regex โดยแปลงประโยคเป็น 'รากศัพท์' ก่อนทำการจับคู่"""
    print("Creating category labels using Lemmatization & Regex...")
    
    lemmatizer = WordNetLemmatizer()
    labels = []
    category_counts = {cat: 0 for cat in CATEGORY_KEYWORDS.keys()}
    no_match_count = 0

    for i, comment in enumerate(comments):
        # 1. ทำความสะอาดเบื้องต้น (ลบสัญลักษณ์)
        text = str(comment).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text) 
        
        # 2. แปลงคำในคอมเมนต์ให้เป็น "รากศัพท์ (Root)" ก่อนให้ Regex ตรวจ
        lemmatized_words = [lemmatizer.lemmatize(word) for word in text.split()]
        comment_lemmatized = ' '.join(lemmatized_words)

        comment_categories = set()

        # 3. ใช้ Regex ค้นหา (ค้นหาจาก comment_lemmatized แทน)
        for category, subcats in CATEGORY_KEYWORDS.items():
            # รวมศัพท์ positive, negative
            all_keywords = []
            for subcat, keywords in subcats.items():
                all_keywords.extend(keywords)
                
            for keyword in all_keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                # ค้นหาในประโยคที่ถูกทำรากศัพท์แล้ว
                if re.search(pattern, comment_lemmatized):
                    comment_categories.add(category)
                    category_counts[category] += 1
                    break # เจอคำเดียวพอ เปลี่ยนไปเช็คหมวดอื่นต่อ

        if not comment_categories:
            no_match_count += 1
        labels.append(comment_categories)

    print("\nCategory Distribution:")
    for cat, count in category_counts.items():
        print(f"  - {cat}: {count} ({(count / len(comments)) * 100:.1f}%)")
    print(f"  - No category matched: {no_match_count} ({(no_match_count/len(comments)*100):.1f}%)")

    return labels


# 2. TRAINING PIPELINE

def train_category_model():
    setup_nltk()
    os.makedirs(CONFIG["model_dir"], exist_ok=True)

    # 1. โหลดข้อมูล
    print(f"\nLoading data from {CONFIG['data_path']}...")
    df = pd.read_csv(CONFIG["data_path"])
    
    if 'comments' not in df.columns:
        raise ValueError("Column 'comments' not found in dataset")
    
    comments = df['comments'].dropna().tolist()
    print(f"Loaded {len(comments)} comments")

    # 2. สร้าง Labels ด้วย Regex
    y_raw = create_category_labels(comments)

    # 3. คัดเอาเฉพาะคอมเมนต์ที่มีอย่างน้อย 1 หมวดหมู่
    valid_indices = [i for i, labels in enumerate(y_raw) if len(labels) > 0]
    comments_filtered = [comments[i] for i in valid_indices]
    y_raw_filtered = [y_raw[i] for i in valid_indices]

    print(f"\nUsing {len(comments_filtered)} labeled comments for training ML model")

    # 4. Binarize labels
    print("Binarizing labels...")
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(y_raw_filtered)

    # 5. แบ่งข้อมูล (Train / Test Split)
    print("\nSplitting data before Vectorization...")
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        comments_filtered, y, 
        test_size=CONFIG["test_size"], 
        random_state=CONFIG["random_seed"]
    )
    
    # 6. ทำความสะอาดข้อความ (Clean text) แยก Train กับ Test
    X_train_clean = clean_text(X_train_text)
    X_test_clean = clean_text(X_test_text)

    # 7. สร้าง Vectorizer ของตัวเอง (Fit เฉพาะ Train Set)
    print("\nVectorizing text with custom TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=CONFIG["max_features"],
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8
    )
    X_train = vectorizer.fit_transform(X_train_clean)
    X_test = vectorizer.transform(X_test_clean)

    print(f"  Training set: {X_train.shape[0]} samples")
    print(f"  Test set: {X_test.shape[0]} samples")

    # 8. เทรนโมเดล
    print("\nTraining OneVsRestClassifier with LogisticRegression...")
    model = OneVsRestClassifier(
        LogisticRegression(max_iter=1000, random_state=CONFIG["random_seed"], class_weight='balanced'),
        n_jobs=-1 
    )
    model.fit(X_train, y_train)

    # 9. ประเมินผล
    print("\n" + "-"*40 + "\nEVALUATION\n" + "-"*40)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # โชว์ Train Accuracy ให้เห็นรอยหยักสมองของโมเดล
    train_acc = (y_train_pred == y_train).mean()
    test_acc = (y_test_pred == y_test).mean()
    test_hamming = hamming_loss(y_test, y_test_pred)

    print(f"Training Exact Match Accuracy : {train_acc:.4f}  <-- เช็ค Overfitting ตรงนี้")
    print(f"Test Exact Match Accuracy     : {test_acc:.4f}")
    print(f"Test Hamming Loss             : {test_hamming:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_test_pred, target_names=mlb.classes_))

    # 10. เซฟโมเดล
    # สำคัญ: ต้องเซฟ Vectorizer แยกตั้งชื่อว่า category_vectorizer.pkl
    vec_path = os.path.join(CONFIG["model_dir"], 'category_vectorizer.pkl')
    mod_path = os.path.join(CONFIG["model_dir"], 'category_model.pkl')
    mlb_path = os.path.join(CONFIG["model_dir"], 'mlb.pkl')

    joblib.dump(vectorizer, vec_path)
    joblib.dump(model, mod_path)
    joblib.dump(mlb, mlb_path)
    print(f"\n✅ Models saved successfully in '{CONFIG['model_dir']}/' directory.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CONFIG["data_path"] = sys.argv[1]

    try:
        train_category_model()
    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)