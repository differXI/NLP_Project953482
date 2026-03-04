# NLP-953482: Course & Instructor Evaluation Analytics System

## 📊 Project Overview

An NLP-powered analytics system for analyzing course and instructor evaluations. The system combines quantitative data analysis with natural language processing to provide comprehensive insights into teaching performance.

**Key Features:**
- 🤖 Sentiment analysis (Positive/Neutral/Negative)
- 🏷️ Multi-label categorization (5 analytical subcategories)
- 📈 Trend analysis with Linear Regression
- 🔮 Future rating prediction
- ⚖️ Professor comparison dashboard
- 🔄 Retrainable models with full training pipeline

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.8+ - [Download](https://www.python.org/downloads/)
- **Node.js** 14+ - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/downloads/)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NLP_Project953482
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

---

## 🎯 First Time Setup - Train Models

**IMPORTANT:** Pre-trained models are included, but if you want to retrain them:

```bash
cd backend

# Option 1: Train all models at once (Recommended)
python train_all.py

# Option 2: Train individually
python train_sentiment.py
python train_categories.py

# Option 3: Test trained models
python evaluate_models.py
```

**Training Process:**
- `train_sentiment.py` - Trains sentiment classifier (Positive/Neutral/Negative)
- `train_categories.py` - Trains multi-label category classifier (5 categories)
- `train_all.py` - Runs both training scripts sequentially
- `evaluate_models.py` - Tests models with sample or custom comments

---

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
python main.py
```

The server will start at: **http://127.0.0.1:8000**

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Start Frontend (New Terminal)

```bash
cd frontend
npm start
```

The application will open at: **http://localhost:3000**

**Expected output:**
```
Compiled successfully!
You can now view frontend in the browser.
  Local:            http://localhost:3000
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /` | API documentation & info |
| `GET /health` | Health check & system status |
| `GET /professors` | List all professors |
| `GET /professor/{name}` | Professor details with analytics |
| `GET /professor/{name}/trend` | Rating trend analysis |
| `GET /professor/{name}/predict?periods=5` | Future rating prediction |
| `GET /search?q=query` | Search professors by name |
| `GET /professors/compare?names=prof1,prof2` | Compare multiple professors |
| `GET /professors/top?by=rating&n=10` | Top N professors |

**Interactive API Docs:** http://127.0.0.1:8000/docs (Swagger UI)

---

## 🎓 Using the Application

### Individual Professor View

1. **Select a Professor** from the sidebar
2. **View Analytics:**
   - Average quality & difficulty ratings
   - Number of ratings
   - Courses taught
   - Sentiment distribution chart
   - Category breakdown chart
   - **Rating Trend Chart** (with prediction)
   - **Trend Direction** (increasing/decreasing/stable)
   - **Model Quality Metrics** (R²)

### Professor Comparison View

1. **Click "📊 Compare Professors" tab**
2. **Select 2-5 Professors** from the list
3. **Click "Compare Professors"**
4. **View:**
   - Comparison table with rankings
   - Rating vs Difficulty bar chart
   - Sentiment comparison chart
   - Multi-dimensional radar chart
   - Top performer indicators

### Search Functionality

- Type in the search bar to filter professors by name
- Search is case-insensitive
- Updates the professor list in real-time

---

## 🏗️ Project Structure

```
NLP_Project953482/
├── backend/                     # Python FastAPI Server
│   ├── main.py                 # API endpoints (8 endpoints)
│   ├── analytics.py            # NLP analysis functions
│   ├── trend_analysis.py       # Trend & prediction logic
│   ├── requirements.txt        # Python dependencies
│   ├── train_sentiment.py      # Sentiment training script
│   ├── train_categories.py     # Category training script
│   ├── train_all.py            # Complete training pipeline
│   ├── evaluate_models.py      # Model testing script
│   ├── data/                   # Dataset directory
│   │   └── RateMyProfessor_Sample.csv (10.8MB)
│   └── models/                 # Pre-trained ML models
│       ├── vectorizer.pkl       # TF-IDF vectorizer
│       ├── sentiment_model.pkl  # Sentiment classifier
│       ├── category_model.pkl   # Category classifier
│       └── mlb.pkl              # MultiLabelBinarizer
│
└── frontend/                   # React Application
    ├── src/
    │   ├── App.jsx             # Main app with view toggle
    │   ├── api.js              # API client functions
    │   ├── index.js            # React entry point
    │   └── components/
    │       ├── SearchBar.jsx          # Search functionality
    │       ├── ProfessorList.jsx      # Professor list
    │       ├── ProfessorCard.jsx      # Individual professor card
    │       ├── Insights.jsx           # Analytics dashboard
    │       ├── TrendChart.jsx         # Trend visualization
    │       └── ComparisonDashboard.jsx  # Comparison UI
    └── package.json               # Node dependencies
```

---

## 📚 Documentation Files

| File | Description |
|------|-------------|
| **[README.md](README.md)** | This file - Quick start guide |
| **[research.md](research.md)** | Complete research, methodology & architecture |
| **[plan.md](plan.md)** | Implementation plan & development roadmap |
| **[result.md](result.md)** | Expected results vs requirements coverage |

---

## 🔨 Training Models

### When to Retrain?

Retrain models when:
1. **New data added** - More comments available
2. **Poor performance** - Model accuracy is low
3. **Category changes** - Need to modify categories
4. **Reproducibility** - Need to verify training process

### Training Process

1. **Prepare Dataset**
   - Ensure `RateMyProfessor_Sample.csv` is in `backend/data/`
   - Format: `professor_name, department_name, star_rating, student_difficult, comments`

2. **Run Training**
   ```bash
   cd backend
   python train_all.py
   ```
   This will:
   - Train sentiment classifier (3 classes)
   - Train category classifier (5 categories)
   - Save models to `models/` directory
   - Display evaluation metrics

3. **Evaluate Models**
   ```bash
   python evaluate_models.py
   ```
   Test with default cases or run in interactive mode:
   ```bash
   python evaluate_models.py -i
   ```

---

## 📊 5 Analytical Categories

| Category | Description | Example Keywords |
|----------|-------------|------------------|
| **Teaching Clarity** | Explanation quality, examples | clear, confusing, understandable |
| **Speaking Pace** | Delivery speed, verbal clarity | too fast, clear voice, rushed |
| **Course Structure** | Organization, syllabus | organized, disorganized, structured |
| **Communication** | Responsiveness, feedback | helpful, unresponsive, responsive |
| **Professional Behavior** | Fairness, respect, ethics | professional, rude, fair grading |

---

## 🐛 Troubleshooting

### Backend Issues

**Error: `ModuleNotFoundError: No module named 'fastapi'`**
```bash
cd backend
pip install -r requirements.txt
```

**Error: `FileNotFoundError: models/vectorizer.pkl`**
```bash
cd backend
python train_all.py
```

**Port 8000 already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Error: `npm command not found`**
```bash
# Install Node.js from https://nodejs.org/
```

**Page shows "Network Error":**
- Ensure backend is running
- Check browser console (F12)
- Verify API URL: http://127.0.0.1:8000

**React shows blank page:**
- Check browser console for errors
- Verify all components are present
- Try clearing cache: `npm start` with force refresh

---

## 📈 Features Implemented

### ✅ Core Features (100% Complete)

1. ✅ **Sentiment Classification**
   - Three-class classification (Positive/Neutral/Negative)
   - TF-IDF vectorization
   - Logistic Regression

2. ✅ **Multi-label Category Classification**
   - 5 analytical subcategories
   - Keyword-based labeling
   - OneVsRestClassifier

3. ✅ **Trend Analysis**
   - Time-series rating analysis
   - Linear Regression trend lines
   - R² model quality metrics

4. ✅ **Prediction Feature**
   - Future rating forecasting
   - Confidence intervals (95%)
   - Configurable prediction periods

5. ✅ **Comparison Dashboard**
   - Compare up to 5 professors
   - Side-by-side statistics
   - Multi-dimensional radar charts

---

## 🎯 Target Users

| User | Benefits |
|------|----------|
| **Students** | View course evaluations, check professor ratings, predict future performance |
| **Instructors** | Review feedback, identify improvement areas, track performance over time |
| **Administrators** | Compare professors, identify top performers, data-driven decisions |
| **Institutions** | Quality assurance, academic planning, evaluation system enhancement |

---

## 📦 Dependencies

### Backend (requirements.txt)

```
# Core Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0

# Data Processing
pandas>=1.5.0
numpy>=1.21.0

# NLP / ML
scikit-learn>=1.3.0
nltk>=3.8.0
joblib>=1.3.0

# API
pydantic>=2.0.0
```

### Frontend (package.json)

```
{
  "dependencies": {
    "react": "^19.2.4",
    "react-scripts": "5.0.1",
    "recharts": "^3.7.0",
    "axios": "^1.13.6"
  }
}
```

---

## 📊 Datasets

### Primary: RateMyProfessor Sample

- **File:** `backend/data/RateMyProfessor_Sample.csv`
- **Size:** ~10.8MB
- **Records:** ~100K+ reviews
- **Columns:** professor_name, department_name, star_rating, student_difficult, comments

### Data Processing

- Columns renamed for consistency
- Rows with missing values dropped
- Up to 50 comments sampled per professor for NLP analysis
- Synthetic dates generated for trend analysis (2022-2024)

---

## 🔄 Development Workflow

### Making Changes

**Backend changes:**
```bash
# Edit backend files
# Server auto-reloads if using uvicorn --reload
# Or restart: Ctrl+C, then python main.py
```

**Frontend changes:**
```bash
# React auto-reloads on save
# Just edit files in frontend/src/
```

### Running Tests

```bash
# Backend: Test NLP models
cd backend
python evaluate_models.py -i  # Interactive mode
python evaluate_models.py     # Default test cases

# Frontend: Check browser console (F12)
# Or: npm test
```

---

## 📚 Additional Resources

- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **scikit-learn:** https://scikit-learn.org/
- **Recharts:** https://recharts.org/

---

## 🤝 Support

For questions or issues:
1. Check the [troubleshooting section](#-troubleshooting)
2. Review [research.md](research.md) for methodology
3. Review [plan.md](plan.md) for implementation details
4. Check API docs at: http://127.0.0.1:8000/docs

---

## ✅ Implementation Status

**Requirements Coverage:** 100% ✅

| Category | Status |
|----------|--------|
| Objectives (5/5) | ✅ Complete |
| Core Features (5/5) | ✅ Complete |
| Target Users (4/4) | ✅ Complete |
| Training Scripts | ✅ Complete |
| Trend Analysis | ✅ Complete |
| Prediction Feature | ✅ Complete |
| Comparison Feature | ✅ Complete |

---

*Last Updated: March 4, 2026*
*Project Status: ✅ Implementation Complete*
*Version: 1.0.0*
