# แผนการพัฒนาโปรเจกต์ NLP-953482
# Development Plan for Course & Instructor Evaluation Analytics System

---

## 📋 ภาพรวม (Overview)

เอกสารนี้ระบุรายละเอียดการพัฒนาโค้ดทั้งหมด เพื่อให้ระบบบรรลุตามวัตถุประสงค์ที่วางไว้ใน project proposal

---

## 🎯 สิ่งที่ต้องพัฒนา (What to Build)

### สถานะปัจจุบัน (Current State)
- ✅ มี pre-trained models (.pkl files)
- ✅ มี FastAPI backend พื้นฐาน
- ✅ มี React frontend พื้นฐาน
- ❌ **ไม่มี training scripts** (CRITICAL!)
- ❌ ไม่มี trend analysis
- ❌ ไม่มี prediction feature
- ❌ ไม่มี comparison features

---

## 🔴 Phase 1: NLP Model Training Infrastructure (CRITICAL - Missing!)

### สิ่งที่ต้องสร้าง (Backend Files)

#### 1.1 `backend/train_sentiment.py`
**จำนวนบรรทัดโดยประมาณ:** 120-150 บรรทัด

**วัตถุประสงค์:**
- Train sentiment classifier (Positive/Negative/Neutral)
- ใช้ rating เป็น label:
  - rating >= 4.0 → Positive
  - 3.0 <= rating < 4.0 → Neutral
  - rating < 3.0 → Negative

**ฟังก์ชันหลัก:**
```python
def load_and_prepare_data():
    """โหลด comments และสร้าง sentiment labels จาก star_rating"""
    # Load CSV
    # Create labels based on rating
    pass

def preprocess_text(text_list):
    """Text preprocessing:
    - Lowercase
    - Remove special characters
    - Remove stopwords
    - Lemmatization
    """
    pass

def train_sentiment_model():
    """Train Logistic Regression for sentiment classification"""
    # TF-IDF Vectorization
    # Train/Test split
    # Train model
    # Evaluate (classification_report, confusion_matrix)
    # Save models (vectorizer.pkl, sentiment_model.pkl)
    pass
```

**Dependencies:** pandas, numpy, scikit-learn, nltk, joblib, re

---

#### 1.2 `backend/train_categories.py`
**จำนวนบรรทัดโดยประมาณ:** 150-200 บรรทัด

**วัตถุประสงค์:**
- Train multi-label category classifier (5 categories)
- ใช้ keyword-based approach สร้าง labels

**Category Keywords Dictionary:**
```python
CATEGORY_KEYWORDS = {
    'teaching_clarity': {
        'positive': ['clear', 'understandable', 'well explained', ...],
        'negative': ['confusing', 'unclear', 'hard to follow', ...]
    },
    'speaking_pace': {
        'positive': ['clear voice', 'good pace', ...],
        'negative': ['too fast', 'rushes', 'too slow', ...]
    },
    'course_structure': {
        'positive': ['organized', 'structured', ...],
        'negative': ['disorganized', 'messy', ...]
    },
    'communication': {
        'positive': ['helpful', 'responsive', ...],
        'negative': ['unresponsive', 'ignores questions', ...]
    },
    'professional_behavior': {
        'positive': ['professional', 'respectful', ...],
        'negative': ['rude', 'unfair', ...]
    }
}
```

**ฟังก์ชันหลัก:**
```python
def create_category_labels(comments):
    """สร้าง labels จาก keyword matching"""
    pass

def train_category_model():
    """Train OneVsRestClassifier + LogisticRegression"""
    # Use same vectorizer as sentiment
    # MultiLabelBinarizer for labels
    # Train model
    # Evaluate
    # Save models (category_model.pkl, mlb.pkl)
    pass
```

---

#### 1.3 `backend/train_all.py`
**จำนวนบรรทัดโดยประมาณ:** 50-80 บรรทัด

**วัตถุประสงค์:**
- Training pipeline ที่รวมทุกอย่างในไฟล์เดียว
- Run ได้ง่ายด้วยคำสั่งเดียว

**ฟังก์ชันหลัก:**
```python
def run_training():
    """Run complete training pipeline"""
    print("Training Sentiment Model...")
    # Call train_sentiment.py

    print("Training Category Model...")
    # Call train_categories.py

    print("Training Complete!")
    pass

if __name__ == "__main__":
    run_training()
```

---

#### 1.4 `backend/evaluate_models.py`
**จำนวนบรรทัดโดยประมาณ:** 100-150 บรรทัด

**วัตถุประสงค์:**
- Test trained models
- Interactive mode สำหรับ test custom comments

**ฟังก์ชันหลัก:**
```python
def load_models():
    """Load all trained models"""
    pass

def test_predictions(test_comments):
    """Test with sample comments"""
    # Predict sentiment
    # Predict categories
    # Display results with confidence scores
    pass

def interactive_mode():
    """Test with custom input"""
    pass
```

---

## 🔴 Phase 2: Trend Analysis & Prediction (Backend)

### สิ่งที่ต้องสร้าง (Backend Files)

#### 2.1 `backend/trend_analysis.py`
**จำนวนบรรทัดโดยประมาณ:** 200-250 บรรทัด

**วัตถุประสงค์:**
- วิเคราะห์ trend ของ rating ตามเวลา
- ทำนาย rating ในอนาคตด้วย Linear Regression
- เปรียบเทียบอาจารย์หลายคน
- หา top professors

**ฟังก์ชันหลัก:**

```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from datetime import datetime, timedelta
import numpy as np

def analyze_rating_trend(professor_name: str, df):
    """
    วิเคราะห์ trend ของ rating ตามเวลา

    Returns:
        {
            "dates": [date1, date2, ...],
            "ratings": [rating1, rating2, ...],
            "trend_line": [trend1, trend2, ...],
            "trend_direction": "increasing" | "decreasing" | "stable",
            "trend_percentage": float,
            "model_quality": {
                "r_squared": float,
                "slope": float
            }
        }
    """
    # Filter data for professor
    # Group by date (if needed)
    # Sort by date
    # Fit Linear Regression
    # Calculate trend direction
    # Return results
    pass

def predict_future_rating(professor_name: str, periods: int, df):
    """
    ทำนาย rating ในอนาคต

    Args:
        professor_name: ชื่ออาจารย์
        periods: จำนวนคาบเวลาที่ต้องการทำนาย (default: 5)

    Returns:
        {
            "historical": {
                "dates": [...],
                "ratings": [...],
                "trend_line": [...]
            },
            "future": {
                "dates": [...],
                "predicted_ratings": [...],
                "lower_bound": [...],
                "upper_bound": [...]
            },
            "model_quality": {...}
        }
    """
    # Get historical data
    # Train Linear Regression
    # Predict future periods
    # Calculate confidence intervals
    # Return results
    pass

def compare_professors(professor_names: list, df):
    """
    เปรียบเทียบอาจารย์หลายคน

    Returns:
        {
            "total_professors": int,
            "professors": [
                {
                    "name": str,
                    "avg_rating": float,
                    "avg_difficulty": float,
                    "num_ratings": int,
                    "positive_percentage": float,
                    "negative_percentage": float,
                    "rating_std": float
                },
                ...
            ],
            "comparison": {
                "highest_rated": str,
                "lowest_rated": str,
                "easiest": str,
                "hardest": str,
                "most_consistent": str
            }
        }
    """
    pass

def get_top_professors(by: str, n: int, min_ratings: int, df):
    """
    ดู top N อาจารย์ตาม criteria ที่เลือก

    Args:
        by: "rating" | "difficulty" | "easiest" | "hardest" |
            "most_reviews" | "most_consistent"
        n: จำนวนอันดับ
        min_ratings: จำนวน rating ขั้นต่ำ

    Returns:
        List of top professors
    """
    pass
```

---

#### 2.2 อัปเดต `backend/main.py`
**สิ่งที่ต้องเพิ่ม:** 80-100 บรรทัด

**New API Endpoints:**

```python
from trend_analysis import (
    analyze_rating_trend,
    predict_future_rating,
    compare_professors,
    get_top_professors
)

# ========= TREND ANALYSIS =========
@app.get("/professor/{name}/trend")
def get_professor_trend(name: str):
    """วิเคราะห์ trend ของ rating ตามเวลา"""
    result = analyze_rating_trend(name, df)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# ========= PREDICTION =========
@app.get("/professor/{name}/predict")
def predict_professor_rating(name: str, periods: int = 5):
    """ทำนาย rating ในอนาคตด้วย Linear Regression"""
    if periods < 1 or periods > 20:
        raise HTTPException(status_code=400, detail="Periods must be between 1 and 20")

    result = predict_future_rating(name, periods, df)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# ========= COMPARE PROFESSORS =========
@app.get("/professors/compare")
def compare_professors_get(names: str):
    """เปรียบเทียบหลายอาจารย์ (comma-separated names)"""
    prof_names = [n.strip() for n in names.split(",")]
    result = compare_professors(prof_names, df)
    if result["total_professors"] == 0:
        raise HTTPException(status_code=404, detail="No valid professors found")
    return result

# ========= TOP PROFESSORS =========
@app.get("/professors/top")
def get_top_professors_endpoint(
    by: str = "rating",
    n: int = 10,
    min_ratings: int = 5
):
    """ดู top N อาจารย์"""
    valid_criteria = ["rating", "difficulty", "easiest", "hardest",
                      "most_reviews", "most_consistent"]
    if by not in valid_criteria:
        raise HTTPException(status_code=400, detail=f"Invalid criteria")
    if n < 1 or n > 50:
        raise HTTPException(status_code=400, detail="n must be between 1 and 50")
    return get_top_professors(by, n, min_ratings, df)
```

---

## 🔴 Phase 3: Frontend - Prediction & Trend Display

### สิ่งที่ต้องสร้าง (Frontend Files)

#### 3.1 `frontend/src/components/TrendChart.jsx`
**จำนวนบรรทัดโดยประมาณ:** 100-120 บรรทัด

**วัตถุประสงค์:**
- แสดงกราฟ trend ของ rating ตามเวลา
- แสดง prediction สำหรับอนาคต
- แสดง confidence intervals

**Components:**
```jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend,
         ResponsiveContainer, CartesianGrid } from "recharts";

export default function TrendChart({ data }) {
  if (!data || data.error) return <Error message />;

  // Check if prediction data exists
  const hasPrediction = data.future && data.future.predicted_ratings;

  // Prepare chart data
  const chartData = hasPrediction
    ? [...historicalData, ...futureData]
    : historicalData;

  return (
    <div className="trend-chart-container">
      <h3>Rating Trend & Prediction</h3>

      {/* Trend Indicator */}
      <div className="trend-indicator">
        {getTrendIcon()} {data.trend_direction}
        ({data.trend_percentage}%)
      </div>

      {/* Line Chart */}
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={[1, 5]} />
          <Tooltip />
          <Legend />

          {/* Actual Ratings */}
          <Line type="monotone" dataKey="actualRating"
                stroke="#8884d8" name="Actual Rating" />

          {/* Trend Line */}
          <Line type="monotone" dataKey="trendLine"
                stroke="#82ca9d" name="Trend Line" />

          {/* Predicted Values */}
          {hasPrediction && (
            <Line type="monotone" dataKey="predictedRating"
                  stroke="#ffc658" strokeDasharray="5 5"
                  name="Predicted" />
          )}
        </LineChart>
      </ResponsiveContainer>

      {/* Model Quality Metrics */}
      {data.model_quality && (
        <div className="model-quality">
          <p>R²: {data.model_quality.r_squared.toFixed(3)}</p>
          <p>Trend: {data.model_quality.slope.toFixed(3)}</p>
        </div>
      )}
    </div>
  );
}
```

**Props:**
- `data`: Trend data object from API

---

#### 3.2 `frontend/src/components/TrendChart.css`
**จำนวนบรรทัดโดยประมาณ:** 60-80 บรรทัด

**Styles:**
```css
.trend-chart-container {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.trend-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
}

.trend-indicator.increasing {
  color: #10b981;
}

.trend-indicator.decreasing {
  color: #ef4444;
}

.model-quality {
  display: flex;
  gap: 24px;
  margin-top: 16px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}
```

---

#### 3.3 `frontend/src/components/ComparisonDashboard.jsx`
**จำนวนบรรทัดโดยประมาณ:** 150-200 บรรทัด

**วัตถุประสงค์:**
- UI สำหรับเปรียบเทียบอาจารย์
- Select up to 5 professors
- แสดง comparison table
- แสดง comparison charts

**Components:**
```jsx
import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
         RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts";
import { compareProfessors } from "../api";

export default function ComparisonDashboard({ availableProfessors }) {
  const [selectedProfs, setSelectedProfs] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);

  const handleCompare = async () => {
    if (selectedProfs.length < 2) {
      alert("Please select at least 2 professors");
      return;
    }
    const response = await compareProfessors(selectedProfs);
    setComparisonData(response.data);
  };

  return (
    <div className="comparison-dashboard">
      {/* Selection Section */}
      <div className="selection-section">
        <h3>Select Professors to Compare (max 5)</h3>
        <div className="professor-pool">
          {availableProfessors.map(prof => (
            <button
              key={prof}
              className={selectedProfs.includes(prof) ? "selected" : ""}
              onClick={() => toggleProfessor(prof)}
            >
              {prof}
            </button>
          ))}
        </div>
        <button onClick={handleCompare}>Compare</button>
      </div>

      {/* Results Section */}
      {comparisonData && (
        <>
          {/* Comparison Table */}
          <table className="comparison-table">
            <thead>
              <tr>
                <th>Professor</th>
                <th>Rating</th>
                <th>Difficulty</th>
                <th>Reviews</th>
                <th>Positive %</th>
              </tr>
            </thead>
            <tbody>
              {comparisonData.professors.map(prof => (
                <tr key={prof.name}>
                  <td>{prof.name}</td>
                  <td>{prof.avg_rating.toFixed(2)}</td>
                  <td>{prof.avg_difficulty.toFixed(2)}</td>
                  <td>{prof.num_ratings}</td>
                  <td>{prof.positive_percentage.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Bar Chart Comparison */}
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={comparisonData.professors}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="avg_rating" fill="#8884d8" name="Rating" />
              <Bar dataKey="avg_difficulty" fill="#82ca9d" name="Difficulty" />
            </BarChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
}
```

---

#### 3.4 `frontend/src/components/ComparisonDashboard.css`
**จำนวนบรรทัดโดยประมาณ:** 80-100 บรรทัด

---

#### 3.5 อัปเดต `frontend/src/api.js`
**สิ่งที่ต้องเพิ่ม:** 15-20 บรรทัด

```javascript
// ========= TREND ANALYSIS =========
export const getProfessorTrend = (name) =>
  axios.get(`${API}/professor/${name}/trend`);

export const predictProfessorRating = (name, periods = 5) =>
  axios.get(`${API}/professor/${name}/predict?periods=${periods}`);

// ========= COMPARISON =========
export const compareProfessors = (names) => {
  const namesStr = Array.isArray(names) ? names.join(",") : names;
  return axios.get(`${API}/professors/compare?names=${namesStr}`);
};

// ========= TOP PROFESSORS =========
export const getTopProfessors = (by = "rating", n = 10, minRatings = 5) =>
  axios.get(`${API}/professors/top?by=${by}&n=${n}&min_ratings=${minRatings}`);
```

---

#### 3.6 อัปเดต `frontend/src/App.jsx`
**สิ่งที่ต้องเพิ่ม/แก้ไข:**

```jsx
import { getProfessors, getProfessor, searchProf,
         getProfessorTrend, predictProfessorRating } from "./api";
import ComparisonDashboard from "./components/ComparisonDashboard";

function App() {
  const [view, setView] = useState("individual"); // "individual" or "comparison"
  const [trendData, setTrendData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);

  const selectProf = async (name) => {
    setView("individual");
    setSelected(name);
    setLoading(true);

    // Fetch data in parallel
    const [detailRes, trendRes, predictionRes] = await Promise.all([
      getProfessor(name),
      getProfessorTrend(name).catch(() => ({ data: null })),
      predictProfessorRating(name, 5).catch(() => ({ data: null }))
    ]);

    setData(detailRes.data);
    setTrendData(trendRes.data);
    setPredictionData(predictionRes.data);
    setLoading(false);
  };

  return (
    <div>
      {/* View Toggle */}
      <div className="view-toggle">
        <button onClick={() => setView("individual")}>
          Individual Professor
        </button>
        <button onClick={() => setView("comparison")}>
          Compare Professors
        </button>
      </div>

      {/* Individual View */}
      {view === "individual" && (
        <>
          <ProfessorList ... />
          <Insights
            data={data}
            trendData={trendData}
            predictionData={predictionData}
          />
        </>
      )}

      {/* Comparison View */}
      {view === "comparison" && (
        <ComparisonDashboard availableProfessors={profs} />
      )}
    </div>
  );
}
```

---

#### 3.7 อัปเดต `frontend/src/components/Insights.jsx`
**สิ่งที่ต้องเพิ่ม:**

```jsx
import TrendChart from "./TrendChart";

export default function Insights({ data, trendData, predictionData }) {
  // Combine trend and prediction data
  const combinedTrendData = predictionData || trendData;

  return (
    <div>
      <h2>{data.professor}</h2>
      <p>Avg Rating: {data.avg_rating}</p>
      <p>Avg Difficulty: {data.avg_difficulty}</p>

      {/* NEW: Trend Chart */}
      {combinedTrendData && <TrendChart data={combinedTrendData} />}

      {/* Existing charts */}
      <h3>Sentiment Distribution</h3>
      <BarChart ... />

      <h3>Categories</h3>
      <BarChart ... />
    </div>
  );
}
```

---

## 🟡 Phase 4: Data Integration (Optional)

### สิ่งที่ต้องสร้าง (Backend Files)

#### 4.1 `backend/data_loader.py`
**จำนวนบรรทัดโดยประมาณ:** 100-120 บรรทัด

**วัตถุประสงค์:**
- Load Coursera dataset
- Normalize และ combine กับ RateMyProfessor

**ฟังก์ชันหลัก:**
```python
def load_coursera(path):
    """Load Coursera dataset"""
    pass

def normalize_datasets(rmp_df, coursera_df):
    """Normalize and combine"""
    pass

def load_combined_dataset():
    """Load and combine both datasets"""
    pass
```

---

## 📊 สรุปไฟล์ที่ต้องสร้าง/แก้ไข

### Backend Files (7 ไฟล์)

| ไฟล์ | สถานะ | บรรทัด | Priority |
|------|--------|--------|----------|
| `train_sentiment.py` | สร้างใหม่ | 120-150 | 🔴 CRITICAL |
| `train_categories.py` | สร้างใหม่ | 150-200 | 🔴 CRITICAL |
| `train_all.py` | สร้างใหม่ | 50-80 | 🔴 CRITICAL |
| `evaluate_models.py` | สร้างใหม่ | 100-150 | 🔴 CRITICAL |
| `trend_analysis.py` | สร้างใหม่ | 200-250 | 🔴 HIGH |
| `main.py` | แก้ไข | +80-100 | 🔴 HIGH |
| `data_loader.py` | สร้างใหม่ | 100-120 | 🟡 MEDIUM |

**Backend รวม:** ~900-1,150 บรรทัดใหม่

### Frontend Files (7 ไฟล์)

| ไฟล์ | สถานะ | บรรทัด | Priority |
|------|--------|--------|----------|
| `TrendChart.jsx` | สร้างใหม่ | 100-120 | 🔴 HIGH |
| `TrendChart.css` | สร้างใหม่ | 60-80 | 🔴 HIGH |
| `ComparisonDashboard.jsx` | สร้างใหม่ | 150-200 | 🟡 MEDIUM |
| `ComparisonDashboard.css` | สร้างใหม่ | 80-100 | 🟡 MEDIUM |
| `api.js` | แก้ไข | +15-20 | 🔴 HIGH |
| `App.jsx` | แก้ไข | +30-40 | 🔴 HIGH |
| `Insights.jsx` | แก้ไข | +10-15 | 🔴 HIGH |

**Frontend รวม:** ~445-575 บรรทัดใหม่

### รวมทั้งหมด: ~1,345-1,725 บรรทัด

---

## 📦 Dependencies ที่ต้องเพิ่ม

### Backend (`requirements.txt`)
```
# เดิมมีอยู่แล้ว
fastapi
uvicorn
pandas
scikit-learn
joblib

# ต้องเพิ่ม
nltk>=3.8.0
numpy>=1.21.0
```

### Frontend (`package.json`)
```
# เดิมมีอยู่แล้ว
react
recharts
axios

# ไม่ต้องเพิ่มอะไร
```

---

## 🚀 ลำดับการพัฒนา (Recommended Order)

### Sprint 1: Model Training (🔴 CRITICAL - Week 1)
1. ✅ สร้าง `train_sentiment.py`
2. ✅ สร้าง `train_categories.py`
3. ✅ สร้าง `train_all.py`
4. ✅ สร้าง `evaluate_models.py`
5. ✅ Run training และ verify

### Sprint 2: Trend & Prediction (🔴 HIGH - Week 2)
1. ✅ สร้าง `trend_analysis.py`
2. ✅ อัปเดต `main.py` (new endpoints)
3. ✅ สร้าง `TrendChart.jsx`
4. ✅ สร้าง `TrendChart.css`
5. ✅ อัปเดต `api.js`
6. ✅ อัปเดต `App.jsx`
7. ✅ อัปเดต `Insights.jsx`

### Sprint 3: Comparison (🟡 MEDIUM - Week 3)
1. ✅ สร้าง `ComparisonDashboard.jsx`
2. ✅ สร้าง `ComparisonDashboard.css`
3. ✅ อัปเดต `main.py` (compare endpoints)
4. ✅ Test comparison

### Sprint 4: Data Integration (🟡 MEDIUM - Optional)
1. ✅ สร้าง `data_loader.py`
2. ✅ Test combined dataset

---

## ⚠️ ข้อควรระวัง

1. **Model Training**
   - ต้องใช้ dataset เดิม (RateMyProfessor)
   - Labeling logic ต้องสอดคล้องกับโมเดลเดิม
   - Save models ทับไฟล์เดิม

2. **Data Processing**
   - Synthetic dates ต้องสร้างให้ realistic
   - Sampling 50 comments เพียงพอสำหรับ performance

3. **Frontend State**
   - Loading states สำคัญ
   - Error handling สำหรับ API calls
   - View toggle ต้อง smooth

4. **API Endpoints**
   - Error handling สำหรับ professor not found
   - Input validation (periods, names)
   - CORS configuration

---

## ✅ Checklist สำหรับ Tracking

### Sprint 1: Model Training
- [ ] train_sentiment.py created
- [ ] train_categories.py created
- [ ] train_all.py created
- [ ] evaluate_models.py created
- [ ] Training successful
- [ ] Models saved to models/
- [ ] Evaluation metrics computed

### Sprint 2: Trend & Prediction
- [ ] trend_analysis.py created
- [ ] Trend endpoint working
- [ ] Prediction endpoint working
- [ ] TrendChart.jsx created
- [ ] Frontend integration complete
- [ ] Charts display correctly

### Sprint 3: Comparison
- [ ] Comparison endpoint working
- [ ] ComparisonDashboard.jsx created
- [ ] Compare functionality works
- [ ] Charts display correctly

### Sprint 4: Data Integration
- [ ] data_loader.py created
- [ ] Coursera data loads
- [ ] Combined dataset works

---

*สร้างเมื่อ: 4 มีนาคม 2026*
*สถานะ: Ready for Implementation*
*Total Files: 14 files (7 backend + 7 frontend)*
*Total Lines: ~1,345-1,725 lines*
