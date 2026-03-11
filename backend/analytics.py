import joblib
import os

#  1. หาตำแหน่งโฟลเดอร์ที่ analytics.py ตั้งอยู่
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#  2. Path ให้ชี้ไปที่โฟลเดอร์ models อย่างแม่นยำ
MODELS_DIR = os.path.join(BASE_DIR, "models")

#  3. โหลดโมเดลด้วย Path เต็ม
sentiment_vectorizer = joblib.load(os.path.join(MODELS_DIR, "vectorizer.pkl"))
category_vectorizer = joblib.load(os.path.join(MODELS_DIR, "category_vectorizer.pkl"))

sentiment_model = joblib.load(os.path.join(MODELS_DIR, "sentiment_model.pkl"))
category_model = joblib.load(os.path.join(MODELS_DIR, "category_model.pkl"))
mlb = joblib.load(os.path.join(MODELS_DIR, "mlb.pkl"))

NEUTRAL_THRESHOLD = 0.20
def analyze_text(text: str):
    X_sent = sentiment_vectorizer.transform([text])
    X_cat = category_vectorizer.transform([text])
    
    # 1. ดึงเปอร์เซ็นต์ความน่าจะเป็นออกมา
    probs = sentiment_model.predict_proba(X_sent)[0]
    sent_classes = list(sentiment_model.classes_)
    prob_neg = probs[sent_classes.index('negative')]
    prob_pos = probs[sent_classes.index('positive')]
    
    # 2. แปลงเป็น Neutral ถ้าระยะห่างของเปอร์เซ็นต์ไม่เกิน 20%
    if abs(prob_pos - prob_neg) <= 0.20:
        sent = 'neutral'
    elif prob_pos > prob_neg:
        sent = 'positive'
    else:
        sent = 'negative'
        
    cats = mlb.inverse_transform(category_model.predict(X_cat))[0]
    
    # แพ็คคะแนนความมั่นใจเก็บไว้ด้วย
    confidence = {"negative": prob_neg, "positive": prob_pos}
    
    # คืนค่า 3 อย่างกลับไปให้ไฟล์อื่นใช้งาน
    return sent, list(cats), confidence
