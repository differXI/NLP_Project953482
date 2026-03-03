# แผนการพัฒนาโปรเจกต์ NLP-953482
# Development Plan for Analytic Categories Review System

---

## 📋 ภาพรวม (Overview)

เอกสารนี้ระบุรายละเอียดการแก้ไขและพัฒนาโค้ดเพื่อให้ระบบบรรลุตามวัตถุประสงค์ที่วางไว้ใน project proposal

---

## 🎯 Phase 2: Quantitative Data Analysis Module (INCOMPLETE)

### Task 2.1: Trend and Time-Series Analysis
**File:** `backend/main.py` → สร้างไฟล์ใหม่ `backend/trend_analysis.py`

**สิ่งที่ต้องทำ:**
1. สร้างฟังก์ชันสำหรับวิเคราะห์ trend ของ rating ตามเวลา
2. ต้องการฟิลด์ `post_date` จาก dataset (ตอนนี้ยังไม่มีการใช้)
3. สร้าง endpoint สำหรับดู trend ของแต่ละอาจารย์

```python
# โครงสร้างที่ต้องเพิ่มใน trend_analysis.py
def analyze_rating_trend(professor_name: str):
    """
    วิเคราะห์ trend การ rating ของอาจารย์ตามเวลา

    Returns:
        - dates: รายการวันที่
        - ratings: รายการคะแนนตามวันที่
        - trend_line: ค่าทำนายจาก linear regression
    """
    pass

def predict_future_rating(professor_name: str, periods: int = 5):
    """
    ทำนาย rating ในอนาคตด้วย Linear Regression

    Args:
        professor_name: ชื่ออาจารย์
        periods: จำนวนคาบเวลาที่ต้องการทำนาย

    Returns:
        - future_dates: วันที่ในอนาคต
        - predicted_ratings: ค่าทำนาย
    """
    pass
```

**API Endpoints ที่ต้องเพิ่ม:**
```python
# เพิ่มใน main.py
@app.get("/professor/{name}/trend")
def get_professor_trend(name: str):
    """ดู trend การ rating ตามเวลาของอาจารย์"""
    pass

@app.get("/professor/{name}/predict")
def predict_professor_rating(name: str, periods: int = 5):
    """ทำนาย rating ในอนาคตของอาจารย์"""
    pass
```

### Task 2.2: Comparative Analysis
**File:** `backend/analytics.py` → เพิ่มฟังก์ชันใหม่

**สิ่งที่ต้องทำ:**
1. เปรียบเทียบค่าเฉลี่ย rating ระหว่างอาจารย์
2. เปรียบเทียบค่าเฉลี่ย difficulty ระหว่างอาจารย์
3. จัดอันดับอาจารย์ตาม criteria ต่างๆ

```python
# โครงสร้างที่ต้องเพิ่ม
def compare_professors(professor_names: list):
    """
    เปรียบเทียบข้อมูลหลายๆ อาจารย์

    Returns:
        Dictionary ที่มี comparison metrics
    """
    pass

def get_top_professors(by: str = "rating", n: int = 10):
    """
    ดู top N อาจารย์ตาม criteria ที่เลือก

    Args:
        by: "rating", "difficulty", "sentiment_positive", etc.
        n: จำนวนอันดับ
    """
    pass
```

**API Endpoint:**
```python
@app.get("/professors/compare")
def compare_professors_api(names: str):
    """เปรียบเทียบหลายอาจารย์ (names เป็น comma-separated)"""
    pass

@app.get("/professors/top")
def get_top_professors_api(by: str = "rating", n: int = 10):
    """ดู top อาจารย์"""
    pass
```

---

## 🎯 Phase 3: NLP Model Training (CRITICAL - MISSING!)

**⚠️ IMPORTANT:** โปรเจกต์ปัจจุบันมีโมเดลที่ train แล้ว (.pkl files) แต่ **ไม่มี training script**
สิ่งนี้ต้องถูกสร้างขึ้นก่อนอย่างอื่น!

### Task 3.1: Sentiment Classification Training
**File:** สร้างไฟล์ใหม่ `backend/train_sentiment.py`

**สิ่งที่ต้องทำ:**
1. Load และ preprocess ข้อมูล comments จาก dataset
2. สร้าง labeled training data สำหรับ sentiment (Positive/Negative/Neutral)
3. Train โมเดล classification (Logistic Regression / SVM / Naive Bayes)
4. Evaluate ด้วย metrics: Accuracy, Precision, Recall, F1-score
5. Save โมเดลเป็น `.pkl` file

```python
# train_sentiment.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

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
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    nltk.download('stopwords')
    nltk.download('wordnet')

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    processed = []
    for text in text_list:
        # Lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize and remove stopwords
        words = [lemmatizer.lemmatize(word) for word in text.split()
                 if word not in stop_words]
        processed.append(' '.join(words))

    return processed

def train_sentiment_model():
    """Train sentiment classification model"""
    print("Loading data...")
    X_raw, y = load_and_prepare_data()

    print("Preprocessing text...")
    X = preprocess_text(X_raw)

    print("Vectorizing...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_vec = vectorizer.fit_transform(X)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training model...")
    model = LogisticRegression(max_iter=1000, multi_class='ovr')
    model.fit(X_train, y_train)

    print("Evaluating...")
    y_pred = model.predict(X_test)
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))

    print("\n=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))

    # Save models
    print("\nSaving models...")
    joblib.dump(vectorizer, 'models/vectorizer.pkl')
    joblib.dump(model, 'models/sentiment_model.pkl')

    print("Done! Models saved to models/")

if __name__ == "__main__":
    train_sentiment_model()
```

### Task 3.2: Multi-Label Category Classification Training
**File:** สร้างไฟล์ใหม่ `backend/train_categories.py`

**สิ่งที่ต้องทำ:**
1. สร้าง labeled training data สำหรับ 5 categories
2. ใช้ keyword-based approach เพื่อสร้าง labels อัตโนมัติ
3. Train multi-label classifier (OneVsRestClassifier + LogisticRegression)
4. Evaluate ด้วย metrics สำหรับ multi-label
5. Save โมเดล

```python
# train_categories.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Category keywords dictionaries
CATEGORY_KEYWORDS = {
    'teaching_clarity': {
        'positive': ['clear', 'understandable', 'well explained', 'easy to follow',
                     'explains well', 'makes sense', 'thorough explanation'],
        'negative': ['confusing', 'unclear', 'hard to follow', 'doesnt explain',
                     'difficult to understand', 'unclear explanation']
    },
    'speaking_pace': {
        'positive': ['clear voice', 'good pace', 'appropriate speed', 'easy to hear'],
        'negative': ['too fast', 'rushes', 'too slow', 'mumbles', 'hard to hear',
                     'speaks too fast', 'rushed', 'dragged on']
    },
    'course_structure': {
        'positive': ['organized', 'structured', 'well planned', 'clear syllabus',
                     'good organization', 'well organized course'],
        'negative': ['disorganized', 'unstructured', 'messy', 'no structure',
                     'poorly organized', 'confusing structure']
    },
    'communication': {
        'positive': ['helpful', 'responsive', 'answers questions', 'accessible',
                     'available', 'great communication', 'quick to respond'],
        'negative': ['unresponsive', 'doesnt answer', 'ignores questions',
                     'hard to reach', 'unavailable', 'poor communication']
    },
    'professional_behavior': {
        'positive': ['professional', 'respectful', 'fair', 'caring', 'understanding'],
        'negative': ['rude', 'unprofessional', 'unfair', 'disrespectful',
                     'biased', 'unfair grading']
    }
}

def create_category_labels(comments):
    """
    สร้าง labels สำหรับ categories โดยใช้ keyword matching

    Returns:
        List of sets แต่ละ set มี categories ที่เกี่ยวข้องกับ comment
    """
    labels = []

    for comment in comments:
        comment_lower = comment.lower()
        comment_categories = set()

        for category, keywords in CATEGORY_KEYWORDS.items():
            # Check if any keyword (positive or negative) appears in comment
            all_keywords = keywords['positive'] + keywords['negative']
            if any(keyword in comment_lower for keyword in all_keywords):
                comment_categories.add(category)

        # If no category matched, assign based on content analysis
        if not comment_categories:
            # Could be neutral comment - assign empty set or most common category
            pass

        labels.append(comment_categories)

    return labels

def train_category_model():
    """Train multi-label category classification model"""
    print("Loading data...")
    df = pd.read_csv("data/RateMyProfessor_Sample.csv")
    df = df[['comments']].dropna()

    comments = df['comments'].tolist()

    print("Creating labels...")
    y_raw = create_category_labels(comments)

    # Filter out comments with no labels (optional)
    valid_indices = [i for i, labels in enumerate(y_raw) if len(labels) > 0]
    comments = [comments[i] for i in valid_indices]
    y_raw = [y_raw[i] for i in valid_indices]

    print(f"Training with {len(comments)} labeled comments")

    # Use same vectorizer as sentiment (or create new one)
    from train_sentiment import preprocess_text, load_and_prepare_data

    print("Preprocessing and vectorizing...")
    # Load or create vectorizer (should be consistent with sentiment model)
    vectorizer = joblib.load('models/vectorizer.pkl')  # Use same vectorizer
    X = preprocess_text(comments)
    X_vec = vectorizer.transform(X)

    # Binarize labels
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(y_raw)

    print(f"Categories: {mlb.classes_}")

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42
    )

    print("Training model...")
    model = OneVsRestClassifier(LogisticRegression(max_iter=1000))
    model.fit(X_train, y_train)

    print("Evaluating...")
    y_pred = model.predict(X_test)
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=mlb.classes_))

    # Save models
    print("\nSaving models...")
    joblib.dump(model, 'models/category_model.pkl')
    joblib.dump(mlb, 'models/mlb.pkl')

    print("Done! Models saved to models/")

if __name__ == "__main__":
    train_category_model()
```

### Task 3.3: Complete Training Pipeline
**File:** สร้างไฟล์ใหม่ `backend/train_all.py`

**สิ่งที่ต้องทำ:**
1. Run ทั้งสอง training scripts ใน pipeline เดียว
2. Log และ save evaluation metrics
3. Create training report

```python
# train_all.py
import subprocess
import datetime

def run_training():
    """Run complete training pipeline"""

    print("=" * 50)
    print("NLP Model Training Pipeline")
    print("=" * 50)
    print(f"Started at: {datetime.datetime.now()}\n")

    # Train sentiment model
    print("\n[1/2] Training Sentiment Model...")
    print("-" * 50)
    result1 = subprocess.run(["python", "train_sentiment.py"], cwd="backend")

    if result1.returncode != 0:
        print("ERROR: Sentiment training failed!")
        return

    # Train category model
    print("\n[2/2] Training Category Model...")
    print("-" * 50)
    result2 = subprocess.run(["python", "train_categories.py"], cwd="backend")

    if result2.returncode != 0:
        print("ERROR: Category training failed!")
        return

    print("\n" + "=" * 50)
    print("Training Complete!")
    print(f"Finished at: {datetime.datetime.now()}")
    print("=" * 50)

if __name__ == "__main__":
    run_training()
```

### Task 3.4: Model Evaluation & Testing Script
**File:** สร้างไฟล์ใหม่ `backend/evaluate_models.py`

```python
# evaluate_models.py
import joblib
import pandas as pd
from train_sentiment import preprocess_text

def load_models():
    """Load all trained models"""
    vectorizer = joblib.load('models/vectorizer.pkl')
    sentiment_model = joblib.load('models/sentiment_model.pkl')
    category_model = joblib.load('models/category_model.pkl')
    mlb = joblib.load('models/mlb.pkl')
    return vectorizer, sentiment_model, category_model, mlb

def test_predictions(test_comments):
    """Test models with sample comments"""
    vectorizer, sentiment_model, category_model, mlb = load_models()

    processed = preprocess_text(test_comments)
    X = vectorizer.transform(processed)

    sentiments = sentiment_model.predict(X)
    categories = mlb.inverse_transform(category_model.predict(X))

    for comment, sentiment, cats in zip(test_comments, sentiments, categories):
        print(f"\nComment: {comment[:100]}...")
        print(f"Sentiment: {sentiment}")
        print(f"Categories: {', '.join(cats) if len(cats) > 0 else 'None'}")

# Sample test cases
TEST_COMMENTS = [
    "The professor explains concepts very clearly and makes difficult topics easy to understand.",
    "He speaks too fast and rushes through the material, hard to follow.",
    "Great course! Well organized and structured. The syllabus was clear.",
    "Very unresponsive to emails and doesn't answer questions during office hours.",
    "Fair grading and respectful to all students. Very professional.",
    "I don't have much to say, it was okay."
]

if __name__ == "__main__":
    print("Testing trained models...")
    test_predictions(TEST_COMMENTS)
```

---

## 🎯 Phase 3: NLP Model Enhancement (OPTIONAL - BERT)

### Task 3.1: BERT Fine-tuning (ADVANCED)
**File:** สร้างไฟล์ใหม่ `backend/train_bert.py`

**สิ่งที่ต้องทำ:**
1. เตรียม training data จาก RateMyProfessor และ Coursera
2. Fine-tune BERT model สำหรับ sentiment classification
3. Fine-tune BERT model สำหรับ multi-label category classification
4. Save และ load BERT models

**โครงสร้างไฟล์:**
```python
# train_bert.py
def prepare_bert_training_data():
    """เตรียมข้อมูลสำหรับ BERT training"""
    pass

def train_sentiment_bert():
    """Fine-tune BERT สำหรับ sentiment"""
    pass

def train_category_bert():
    """Fine-tune BERT สำหรับ multi-label categories"""
    pass

def save_bert_models():
    """บันทึก models"""
    pass
```

**อัปเดต analytics.py:**
```python
# เพิ่ม option ในการเลือกใช้ BERT หรือ traditional ML
def analyze_text(text: str, use_bert: bool = False):
    if use_bert:
        return analyze_with_bert(text)
    else:
        return analyze_with_traditional_ml(text)
```

---

## 🎯 Phase 4: Frontend Enhancement

### Task 4.1: Trend Visualization Component
**File:** สร้างไฟล์ใหม่ `frontend/src/components/TrendChart.jsx`

**สิ่งที่ต้องทำ:**
1. สร้าง LineChart แสดง trend ของ rating ตามเวลา
2. แสดง trend line จาก Linear Regression
3. แสดง predicted values สำหรับอนาคต

```jsx
// โครงสร้าง TrendChart.jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend } from "recharts";

export default function TrendChart({ data }) {
  // data: { dates, ratings, trendLine, predictedDates, predictedRatings }
  return (
    <LineChart width={600} height={300} data={data}>
      {/* Actual ratings */}
      <Line type="monotone" dataKey="ratings" stroke="#8884d8" name="Actual Rating" />
      {/* Trend line */}
      <Line type="monotone" dataKey="trendLine" stroke="#82ca9d" name="Trend Line" />
      {/* Predicted values */}
      <Line type="monotone" dataKey="predictedRatings" stroke="#ffc658" strokeDasharray="5 5" name="Predicted" />
    </LineChart>
  );
}
```

**อัปเดต App.jsx:**
```jsx
import TrendChart from "./components/TrendChart";

// ภายใน App component
const [trendData, setTrendData] = useState(null);

const selectProf = async (name) => {
  setSelected(name);
  getProfessor(name).then(r => setData(r.data));
  // เพิ่ม: ดึง trend data
  getProfessorTrend(name).then(r => setTrendData(r.data));
};

// ใน JSX
<TrendChart data={trendData} />
```

**อัปเดต api.js:**
```javascript
export const getProfessorTrend = (name) => axios.get(`${API}/professor/${name}/trend`);
export const predictProfessorRating = (name, periods = 5) =>
  axios.get(`${API}/professor/${name}/predict?periods=${periods}`);
```

### Task 4.2: Comparison Dashboard Component
**File:** สร้างไฟล์ใหม่ `frontend/src/components/ComparisonDashboard.jsx`

**สิ่งที่ต้องทำ:**
1. แสดงตารางเปรียบเทียบอาจารย์หลายคน
2. แสดงกราฟเปรียบเทียบ (Bar chart แบบ grouped)
3. ให้เลือกอาจารย์ที่ต้องการเปรียบเทียบ

```jsx
// โครงสร้าง ComparisonDashboard.jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from "recharts";

export default function ComparisonDashboard({ professors }) {
  // professors: array of professor objects for comparison

  return (
    <div>
      <h2>Professor Comparison</h2>
      <BarChart width={600} height={300} data={professors}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="avg_rating" fill="#8884d8" name="Avg Rating" />
        <Bar dataKey="avg_difficulty" fill="#82ca9d" name="Avg Difficulty" />
      </BarChart>
    </div>
  );
}
```

### Task 4.3: Enhanced Insights Component
**File:** แก้ไข `frontend/src/components/Insights.jsx`

**สิ่งที่ต้องเพิ่ม:**
1. เพิ่ม predicted rating display
2. เพิ่ม trend indicator (increasing/decreasing)
3. เพิ่ม recommendation based on sentiment

```jsx
// เพิ่มใน Insights component
<div className="prediction-section">
  <h3>Predicted Future Rating</h3>
  <p>Trend: {data.trend_direction} ({data.trend_percentage}%)</p>
  <p>Predicted (next semester): {data.predicted_rating}</p>
</div>
```

---

## 🎯 Phase 5: Data Integration

### Task 5.1: Coursera Dataset Integration
**File:** สร้างไฟล์ใหม่ `backend/data_loader.py`

**สิ่งที่ต้องทำ:**
1. Load และ preprocess Coursera dataset
2. Combine กับ RateMyProfessor data
3. Normalize format ให้สอดคล้องกัน

```python
# data_loader.py
def load_coursera_data(path: str):
    """
    Load Coursera course reviews

    Returns:
        DataFrame ที่ normalized แล้ว
    """
    pass

def combine_datasets(rmp_df, coursera_df):
    """
    รวมสอง datasets เข้าด้วยกัน

    Returns:
        Combined DataFrame
    """
    pass

def save_combined_dataset(output_path: str):
    """บันทึก combined dataset"""
    pass
```

**อัปเดต main.py:**
```python
# แก้ไขส่วน load data
from data_loader import load_coursera_data, combine_datasets

rmp_df = pd.read_csv("data/RateMyProfessor_Sample.csv")
coursera_df = load_coursera_data("data/Coursera_reviews.csv")
df = combine_datasets(rmp_df, coursera_df)
```

---

## 📝 สรุปการแก้ไขไฟล์

### ไฟล์ที่ต้องสร้างใหม่ (New Files)

| ไฟล์ | จำนวนบรรทัดโดยประมาณ | Priority |
|------|------------------------|----------|
| `backend/train_sentiment.py` | ~80-100 | 🔴 CRITICAL |
| `backend/train_categories.py` | ~100-120 | 🔴 CRITICAL |
| `backend/train_all.py` | ~30-40 | 🔴 CRITICAL |
| `backend/evaluate_models.py` | ~50-60 | 🔴 CRITICAL |
| `backend/trend_analysis.py` | ~80-100 | 🔴 HIGH |
| `backend/data_loader.py` | ~60-80 | 🟡 MEDIUM |
| `backend/train_bert.py` | ~150-200 | 🟢 LOW (OPTIONAL) |
| `frontend/src/components/TrendChart.jsx` | ~40-50 | 🔴 HIGH |
| `frontend/src/components/ComparisonDashboard.jsx` | ~50-60 | 🟡 MEDIUM |

### ไฟล์ที่ต้องแก้ไข (Modified Files)

| ไฟล์ | สิ่งที่ต้องเพิ่ม | จำนวนบรรทัดที่เพิ่มโดยประมาณ |
|------|--------------|-----------------------------|
| `backend/main.py` | Trend & prediction endpoints, comparison endpoints | ~30-40 |
| `backend/analytics.py` | Comparison functions | ~20-30 |
| `frontend/src/App.jsx` | Trend state, comparison state | ~15-20 |
| `frontend/src/components/Insights.jsx` | Prediction display, trend indicator | ~10-15 |
| `frontend/src/api.js` | New API calls | ~5-10 |

---

## 🚀 ลำดับการพัฒนาที่แนะนำ (Suggested Order)

### Sprint 0: NLP Model Training (🔴 CRITICAL - MUST DO FIRST!)
**⚠️ ต้องทำก่อนอื่น! ปัจจุบันไม่มี training scripts**

1. ✅ สร้าง `backend/train_sentiment.py`
2. ✅ สร้าง `backend/train_categories.py`
3. ✅ สร้าง `backend/train_all.py` (training pipeline)
4. ✅ สร้าง `backend/evaluate_models.py` (testing framework)
5. ✅ Run training และบันทึก metrics
6. ✅ Document training process

### Sprint 1: Core Trend Analysis (🔴 HIGH PRIORITY)
1. ✅ สร้าง `backend/trend_analysis.py`
2. ✅ เพิ่ม endpoints ใน `backend/main.py`
3. ✅ สร้าง `frontend/src/components/TrendChart.jsx`
4. ✅ อัปเดต `frontend/src/App.jsx` และ `frontend/src/api.js`

### Sprint 2: Comparison Features (🟡 MEDIUM PRIORITY)
1. ✅ เพิ่ม comparison functions ใน `backend/analytics.py`
2. ✅ เพิ่ม comparison endpoints ใน `backend/main.py`
3. ✅ สร้าง `frontend/src/components/ComparisonDashboard.jsx`

### Sprint 3: Data Integration (🟡 MEDIUM PRIORITY)
1. ✅ สร้าง `backend/data_loader.py`
2. ✅ อัปเดต `backend/main.py` ให้ load combined dataset

### Sprint 4: BERT Enhancement (🟢 LOW - OPTIONAL)
1. ✅ สร้าง `backend/train_bert.py`
2. ✅ อัปเดต `backend/analytics.py` ให้รองรับ BERT

---

## 📦 Dependencies ที่ต้องเพิ่ม

### Backend (requirements.txt)
```
# สำหรับ NLP training (CRITICAL - Sprint 0)
scikit-learn>=1.0.0
numpy>=1.21.0
nltk>=3.8.0
pandas>=1.5.0
joblib>=1.3.0

# สำหรับ trend analysis
scikit-learn>=1.0.0
numpy>=1.21.0

# สำหรับ BERT (ถ้าทำ Sprint 4)
torch>=2.0.0
transformers>=4.30.0
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "recharts": "^2.8.0",  // มีอยู่แล้ว
    "axios": "^1.4.0"      // มีอยู่แล้ว
  }
}
```

---

## ⚠️ ข้อควรระวัง (Important Notes)

1. **Dataset Issue:** RateMyProfessor sample อาจไม่มีฟิลด์ `post_date` ต้องตรวจสอบและ preprocess ก่อน
2. **Model Performance:** BERT fine-tuning ต้องการ GPU และเวลา training นาน
3. **API Rate Limit:** Coursera data อาจมีข้อจำกัดในการดึงข้อมูล
4. **Testing:** ต้อง test กับข้อมูลจริงหลังจาก implement แต่ละ sprint

---

## ✅ Checklist สำหรับ Tracking Progress

- [ ] **Sprint 0: NLP Model Training (CRITICAL - DO FIRST!)**
  - [ ] train_sentiment.py created
  - [ ] train_categories.py created
  - [ ] train_all.py created
  - [ ] evaluate_models.py created
  - [ ] Training executed successfully
  - [ ] Models tested with sample data
  - [ ] Training metrics documented

- [ ] Sprint 1: Trend Analysis
  - [ ] trend_analysis.py created
  - [ ] Trend endpoints working
  - [ ] TrendChart component created
  - [ ] Frontend integration complete

- [ ] Sprint 2: Comparison Features
  - [ ] Comparison functions implemented
  - [ ] Comparison endpoints working
  - [ ] ComparisonDashboard created
  - [ ] UI integrated

- [ ] Sprint 3: Data Integration
  - [ ] Coursera data loader created
  - [ ] Datasets combined successfully
  - [ ] Combined data tested

- [ ] Sprint 4: BERT Enhancement (OPTIONAL)
  - [ ] BERT training script created
  - [ ] Models trained and saved
  - [ ] BERT inference working
  - [ ] Performance compared with traditional ML

---

*สร้างเมื่อ: 3 มีนาคม 2026*
*สถานะ: Ready for Implementation*
