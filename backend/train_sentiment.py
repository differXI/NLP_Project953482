"""
Sentiment Classification Training Script
- Cleans and preprocesses review texts.
- Trains a Logistic Regression model (TF-IDF features).
- Classifies into: Positive (>= 4.0), Neutral (3.0 - 3.9), Negative (< 3.0).
"""

import os
import re
import sys
import nltk
import joblib
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ==========================================
# ⚙️ SETTINGS (ปรับแก้ค่าต่างๆ ได้ตรงนี้เลย)
# ==========================================
CONFIG = {
    "data_path": os.path.join(BASE_DIR, "data", "RateMyProfessor_Sample.csv"),
    "model_dir": os.path.join(BASE_DIR, "models"),
    "test_size": 0.2,                                 # สัดส่วนข้อมูลเทส (20%)
    "max_features": 5000,                             # จำนวนคำสูงสุดที่ให้โมเดลจำ (TF-IDF)
    "random_seed": 42                                 # ล็อคผลลัพธ์ให้เหมือนเดิมทุกครั้งที่รัน
}

# ==========================================
# 1. SETUP & PREPARATION
# ==========================================
def setup_nltk():
    """ดาวน์โหลดข้อมูล NLTK ที่จำเป็น (ถ้ายังไม่มี)"""
    try:
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading NLTK data...")
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)

def load_data(filepath):
    """โหลดข้อมูลและสร้าง Label ความรู้สึก"""
    print(f"Loading data from {filepath}...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")

    df = pd.read_csv(filepath)
    
    # เช็คว่ามีคอลัมน์ที่ต้องการไหม
    if not all(col in df.columns for col in ['student_star', 'comments']):
        raise ValueError("Dataset must contain 'student_star' and 'comments' columns.")

    # ลบแถวที่ว่างทิ้ง
    df = df[['student_star', 'comments']].dropna()
    print(f"Loaded {len(df)} valid reviews.")

    # กำหนดเกณฑ์คะแนน (แก้เกณฑ์ตรงนี้ได้เลยถ้าต้องการ)
    def assign_sentiment(rating):
        if rating >= 4.0: return 'positive'
        if rating <= 2.5: return 'negative'
        return 'drop' # กำหนดคลาสที่จะทิ้ง
        
    df['sentiment'] = df['student_star'].apply(assign_sentiment)
    # ตัดแถวที่เป็น 'drop' ออกจากการเทรน
    df = df[df['sentiment'] != 'drop']
    
    print("\nLabel Distribution:")
    print(df['sentiment'].value_counts())
    
    return df['comments'].tolist(), df['sentiment'].tolist()

def clean_text(texts):
    """ทำความสะอาดข้อความ (ลบสัญลักษณ์, ตัวเลข, stop words และทำ lemmatization)"""
    print("\nPreprocessing text... (This might take a while)")
    stop_words = set(stopwords.words('english'))
    negation_words = {"not", "no", "nor", "doesn't", "isn't", "didn't", "wasn't", "wouldn't", "can't", "cannot", "couldn't", "won't"}
    stop_words = stop_words - negation_words
    lemmatizer = WordNetLemmatizer()
    processed = []

    for i, text in enumerate(texts):
        if i % 5000 == 0 and i > 0:
            print(f"  Processed {i} texts...")

        # แปลงเป็นพิมพ์เล็ก ลบอักขระพิเศษและตัวเลข
        text = text.replace('-', ' ')
        text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
        
        # ตัดคำ (Tokenize), ลบ Stop words, และจัดรูปคำ (Lemmatize)
        words = [
            lemmatizer.lemmatize(word) for word in text.split() 
            if word not in stop_words and len(word) > 2
        ]
        processed.append(' '.join(words))

    return processed

# ==========================================
# 2. TRAINING PIPELINE
# ==========================================
def train_model():
    """รันขั้นตอนการเทรนทั้งหมด"""
    setup_nltk()
    os.makedirs(CONFIG["model_dir"], exist_ok=True)

    # 1. โหลดข้อมูล
    X_raw, y = load_data(CONFIG["data_path"])

    # 2. ทำความสะอาดข้อความ
    X_cleaned = clean_text(X_raw)

    # 3. แบ่งข้อมูล Train / Test ทันทีก่อนทำ TF-IDF (แก้ Data Leakage)
    print("\nSplitting data...")
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        X_cleaned, y, 
        test_size=CONFIG["test_size"], 
        random_state=CONFIG["random_seed"], 
        stratify=y
    )

    # 4. แปลงข้อความเป็นตัวเลข (TF-IDF)
    print("Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=CONFIG["max_features"],
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8
    )
    
    # 🔥 จุดสำคัญ: Fit เฉพาะชุด Train เท่านั้น
    X_train = vectorizer.fit_transform(X_train_text)
    
    # ส่วนชุด Test ให้ทำแค่ Transform (ห้าม fit เด็ดขาด)
    X_test = vectorizer.transform(X_test_text)

    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")

    # 5. เทรนโมเดล Logistic Regression
    print("\nTraining Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        multi_class='multinomial',
        solver='lbfgs',
        random_state=CONFIG["random_seed"],
    )
    model.fit(X_train, y_train)

    # 6. ประเมินผล
    print("\n" + "-"*40 + "\nEVALUATION\n" + "-"*40)
    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    
    print(f"Test Accuracy: {test_acc:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # 7. เซฟโมเดล
    vec_path = os.path.join(CONFIG["model_dir"], 'vectorizer.pkl')
    mod_path = os.path.join(CONFIG["model_dir"], 'sentiment_model.pkl')
    
    joblib.dump(vectorizer, vec_path)
    joblib.dump(model, mod_path)
    print(f"\nModels saved successfully in '{CONFIG['model_dir']}/' directory.")
    
    return test_acc

# ==========================================
# 3. EXECUTION
# ==========================================
if __name__ == "__main__":
    # รองรับการรับ path ผ่าน command line: python train_sentiment.py ./my_data.csv
    if len(sys.argv) > 1:
        CONFIG["data_path"] = sys.argv[1]
        
    try:
        train_model()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)