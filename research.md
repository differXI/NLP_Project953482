# NLP-953482: Analytic Categories Review System for Course and Instructor Evaluation

## Project Overview

**Project Title:** Analytic Categories Review System for Course and Instructor Evaluation Result

**Objective:** Develop an NLP-powered system that analyzes both quantitative (numerical ratings) and qualitative (textual comments) evaluation data to provide comprehensive insights for teaching improvement and academic decision-making.

---

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [System Objectives](#system-objectives)
3. [Methodology](#methodology)
4. [Technical Architecture](#technical-architecture)
5. [Current Implementation Status](#current-implementation-status)
6. [Proposed Features](#proposed-features)
7. [Development Milestones](#development-milestones)
8. [Datasets](#datasets)
9. [Technology Stack](#technology-stack)
10. [🎉 Implementation Complete - March 2026](#implementation-complete---march-2026)

---

## Problem Statement

### Four Key Challenges:

1. **Limited Interpretability of Numerical Scores**
   - Numerical ratings summarize satisfaction but lack contextual explanations
   - Cannot identify specific causes behind evaluation results

2. **Manual Analysis of Textual Feedback**
   - Time-consuming and labor-intensive
   - Difficult to standardize
   - Inconsistent across reviewers

3. **Lack of Structured Categorization**
   - Existing systems focus only on overall sentiment (positive/negative)
   - Cannot identify specific aspects of teaching performance systematically

4. **Inconsistent Interpretation**
   - Manual interpretation introduces subjectivity
   - Different evaluators may interpret the same comment differently

---

## System Objectives

1. Analyze structured evaluation data using standard statistical methods
2. Classify open-ended textual feedback into positive, negative, and neutral sentiment
3. Detect and categorize multiple issues within a single comment
4. Organize feedback into meaningful subcategories for deeper analysis
5. **Predict future instructor and course popularity trends** based on historical data

---

## Methodology

### 1. Quantitative Data Analysis
Focuses on structured evaluation data:
- Rating-scale questions (1-5 scale)
- Multiple-choice questions

**Analysis Techniques:**
- Descriptive statistics (mean, distribution, frequency)
- Comparative analysis across evaluation criteria
- **Trend and Time-Series Analysis**
- **Linear Regression for forecasting future results**

### 2. NLP-Based Qualitative Text Analysis

#### AI Techniques Used:

**2.1 Supervised Learning**
- Sentiment classification (Positive / Negative / Neutral)
- Multi-label subcategory classification
- **Possible Models:** Logistic Regression, SVM, BERT

**2.2 Feature Representation**
- TF-IDF vectorization
- Word embeddings (optional)

**2.3 Rule-Based Support (Hybrid Approach)**
- Keyword dictionaries for strengthening classification consistency

#### Sentiment Classification
- **Type:** Multi-class classification
- **Labels:** Positive, Negative, Neutral
- **Models:** Logistic Regression, SVM, Multinomial Naive Bayes
- **Metrics:** Accuracy, Precision, Recall, F1-score

#### Multi-Issue Detection
- Identifies multiple opinions/concerns within a single comment
- Example: Comment may mention both teaching clarity AND speaking pace issues

#### Subcategory Classification (5 Categories)

| Category | Description | Positive Keywords | Negative Keywords |
|----------|-------------|-------------------|-------------------|
| **Teaching Clarity** | Explanation quality, examples, logical flow | clear, well explained, understandable | confusing, unclear, difficult to follow |
| **Speaking Pace** | Delivery speed, verbal presentation | clear voice, appropriate pace | too fast, rushed, too slow |
| **Course Structure** | Organization, syllabus, assignments, workload | organized, structured, well planned | messy, disorganized, heavy workload |
| **Communication Effectiveness** | Interaction, responsiveness, feedback | helpful, responsive, supportive | ignores questions, unresponsive |
| **Professional Behavior** | Punctuality, fairness, respect, ethics | professional, respectful, fair | late, rude, unfair grading |

---

## Technical Architecture

### Backend (Python/FastAPI)
```
backend/
├── main.py              # FastAPI application & API endpoints
├── analytics.py         # NLP analysis functions
├── requirements.txt     # Python dependencies
├── data/                # Dataset storage
│   └── RateMyProfessor_Sample.csv
└── models/              # Trained ML models
    ├── vectorizer.pkl   # TF-IDF vectorizer
    ├── sentiment_model.pkl  # Sentiment classifier
    ├── category_model.pkl   # Category classifier
    └── mlb.pkl          # MultiLabelBinarizer
```

### Frontend (React)
```
frontend/
├── src/
│   ├── App.jsx                    # Main application component
│   ├── api.js                     # API client functions
│   └── components/
│       ├── SearchBar.jsx          # Search functionality
│       ├── ProfessorList.jsx      # List of professors
│       ├── ProfessorCard.jsx      # Individual professor card
│       └── Insights.jsx           # Analytics visualization
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/professors` | GET | Get all professor names |
| `/professor/{name}` | GET | Get detailed analytics for a professor |
| `/search` | GET | Search professors by name |

---

## Current Implementation Status

### ✅ Completed Features

1. **Backend API**
   - FastAPI server with CORS support
   - Data loading from RateMyProfessor dataset
   - Three main endpoints (professors list, professor details, search)

2. **NLP Analysis Module**
   - Text analysis using pre-trained models
   - Sentiment prediction (Positive/Negative/Neutral)
   - Multi-label category classification
   - TF-IDF vectorization

3. **Frontend Interface**
   - React application with component-based architecture
   - Search bar for finding professors
   - Professor list display
   - Analytics dashboard with:
     - Average rating display
     - Average difficulty display
     - Sentiment distribution bar chart
     - Category distribution bar chart

### ❌ Missing Critical Components

**⚠️ CRITICAL GAP:** Training scripts for NLP models do NOT exist

The project has pre-trained model files (`.pkl`) but lacks:
- **Training script for Sentiment Classification** (`train_sentiment.py`)
- **Training script for Category Classification** (`train_categories.py`)
- **Model evaluation script** (`evaluate_models.py`)
- **Documentation on model training process**

This means:
- Models cannot be retrained with new data
- No reproducibility of model creation
- Cannot update models with additional datasets (Coursera)
- Training methodology is undocumented

### Data Processing Pipeline

```
Raw CSV Data
    ↓
Filter & Rename Columns
    ↓
Sample Comments (max 50 per professor)
    ↓
TF-IDF Vectorization
    ↓
Sentiment Classification → [Positive, Negative, Neutral]
    ↓
Category Classification → [5 categories]
    ↓
Aggregation & Visualization
```

---

## Proposed Features

### Core Features (Planned)
- [x] Analysis of structured and unstructured evaluation data
- [x] Automatic sentiment detection (positive/negative/neutral)
- [x] Multi-label classification for comments with multiple issues
- [x] Categorization into 5 analytical subcategories
- [x] Aggregated reporting and visualization
- [ ] **Predictive trend analysis for instructor/course popularity**
- [ ] Time-series visualization of rating trends
- [ ] Instructor comparison dashboard

### Target Users
1. **Students** – View course and teaching evaluation results
2. **Instructors** – Review aggregated feedback for teaching improvement
3. **Academic Administrators** – Support academic planning and quality assessment
4. **Educational Institutions** – Enhance evaluation systems and quality assurance

---

## Development Milestones

### Phase 1: Requirement Analysis and Data Preparation ✅
- [x] Review evaluation system requirements
- [x] Define analytical categories (5 subcategories)
- [x] Prepare datasets (RateMyProfessor, Coursera)

### Phase 2: Quantitative Data Analysis Module 🚧
- [x] Basic statistical analysis (mean, distribution)
- [ ] Comparative analysis across evaluation criteria
- [ ] **Trend and Time-Series Analysis** (PENDING)
- [ ] **Linear Regression for forecasting** (PENDING)

### Phase 3: NLP Model Development 🚧
- [x] Sentiment classification model (pre-trained, no training script)
- [x] Multi-label category classification model (pre-trained, no training script)
- [x] TF-IDF vectorization (pre-trained, no training script)
- [ ] **Training scripts for all models (CRITICAL - MISSING)**
- [ ] Model evaluation and testing framework
- [ ] Training documentation and reproducibility
- [ ] Potential BERT fine-tuning for better accuracy (OPTIONAL)

### Phase 4: System Integration and Testing ✅
- [x] Integrate quantitative and NLP-based analysis
- [x] Basic frontend-backend integration
- [ ] Comprehensive testing with sample data
- [ ] Performance evaluation

### Phase 5: Result Analysis and Documentation 🚧
- [x] Basic visualization of results
- [ ] Advanced analytics dashboard
- [ ] Final documentation
- [ ] Presentation materials

---

## Datasets

1. **RateMyProfessor.com Dataset**
   - Source: Big data from professor teaching evaluations
   - Fields: professor_name, department_name, star_rating, student_difficult, comments
   - Current use: Main data source for testing

2. **Coursera Course Reviews Dataset**
   - Size: 100K reviews
   - Planned use: Additional training/testing data

---

## Technology Stack

### Backend
- **Framework:** FastAPI
- **Data Processing:** pandas
- **NLP/ML:** scikit-learn, NLTK/spaCy
- **Model Persistence:** joblib

### Frontend
- **Framework:** React
- **Charts:** Recharts
- **HTTP Client:** Axios
- **Build Tool:** Vite/Create React App

### AI/ML Models
- **Vectorization:** TF-IDF
- **Sentiment Classification:** Logistic Regression / SVM / Naive Bayes
- **Category Classification:** Multi-label classifier with MultiLabelBinarizer

---

## Expected Results

1. ✅ Functional analytic system processing both quantitative and qualitative data
2. ✅ Clear identification of positive/negative sentiment trends
3. ✅ Structured categorization of comments into actionable subcategories
4. 🚧 **Predictive model for instructor/course popularity trends** (IN PROGRESS)
5. ✅ Improved interpretability of student feedback

---

## Limitations

1. **Data Quality Dependency**
   - Accuracy depends on training data quality, diversity, and consistency

2. **Language Understanding**
   - May struggle with sarcasm, irony, or implicit meanings

3. **Predefined Categories**
   - Feedback limited to predefined sentiment labels and 5 subcategories
   - May not cover all possible issues

4. **Dataset Coverage**
   - Currently using RateMyProfessor data
   - Coursera dataset not yet integrated

---

## Key Files Reference

| File | Purpose | Lines |
|------|---------|-------|
| [backend/main.py](backend/main.py) | FastAPI server, API endpoints, data processing | 64 |
| [backend/analytics.py](backend/analytics.py) | NLP model loading and text analysis | 13 |
| [frontend/src/App.jsx](frontend/src/App.jsx) | Main React app, state management | 38 |
| [frontend/src/components/Insights.jsx](frontend/src/components/Insights.jsx) | Analytics visualization with charts | 33 |
| [frontend/src/components/SearchBar.jsx](frontend/src/components/SearchBar.jsx) | Search functionality | N/A |
| [frontend/src/api.js](frontend/src/api.js) | API client functions | 8 |

---

## Next Steps (Prioritized)

1. **🔴 CRITICAL:** Create training scripts for NLP models (train_sentiment.py, train_categories.py)
2. **🔴 CRITICAL:** Add model evaluation and testing framework
3. **🔴 HIGH PRIORITY:** Implement trend prediction with Linear Regression
4. **🔴 HIGH PRIORITY:** Add time-series visualization for rating trends
5. **🟡 MEDIUM:** Integrate Coursera dataset for additional training
6. **🟡 MEDIUM:** Add instructor comparison feature
7. **🟢 LOW:** Explore BERT fine-tuning for improved accuracy
8. **🟢 LOW:** Enhance UI/UX with more interactive dashboards

---

## 🎉 Implementation Complete - March 2026

### ✅ All Critical Features Implemented!

**Status:** All planned features from `plan.md` have been successfully implemented.

#### Completed Sprints:

| Sprint | Priority | Status | Key Deliverables |
|--------|----------|--------|------------------|
| Sprint 0 | 🔴 CRITICAL | ✅ Complete | NLP Training Scripts (4 files) |
| Sprint 1 | 🔴 HIGH | ✅ Complete | Trend Analysis & Prediction (4 files) |
| Sprint 2 | 🟡 MEDIUM | ✅ Complete | Comparison Dashboard (2 files) |
| Sprint 3 | 🟡 MEDIUM | ✅ Complete | Data Integration (1 file) |

#### New Files Created (13 total):

**Backend (9 files):**
- `train_sentiment.py` - Sentiment classification training
- `train_categories.py` - Multi-label category training
- `train_all.py` - Complete training pipeline
- `evaluate_models.py` - Model testing framework
- `trend_analysis.py` - Linear regression trend analysis
- `data_loader.py` - Coursera data integration
- `main.py` - Updated with new endpoints
- `requirements.txt` - Updated dependencies

**Frontend (4 files):**
- `components/TrendChart.jsx` - Trend visualization
- `components/TrendChart.css` - Trend chart styles
- `components/ComparisonDashboard.jsx` - Professor comparison
- `components/ComparisonDashboard.css` - Comparison styles
- `App.jsx` - Updated with view toggle
- `App.css` - Main app styles
- `components/Insights.jsx` - Updated with trend integration
- `components/Insights.css` - Enhanced insights styles

#### Requirements Coverage:

| Requirement | Status |
|-------------|--------|
| Analyze structured evaluation data | ✅ 100% |
| Classify sentiment (pos/neg/neutral) | ✅ 100% |
| Detect multiple issues | ✅ 100% |
| 5 analytical subcategories | ✅ 100% |
| **Predict future popularity trends** | ✅ **100% (NEW!)** |
| Compare professors | ✅ 100% |
| Training scripts | ✅ 100% (CRITICAL FIX) |
| Reproducibility | ✅ 100% |

#### Usage:

```bash
# 1. Train models (first time only)
cd backend
python train_all.py

# 2. Start backend
python main.py

# 3. Start frontend (another terminal)
cd frontend
npm install
npm run dev
```

See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for full details.

---

*Last Updated: March 3, 2026*
*Project Status: ✅ IMPLEMENTATION COMPLETE*
*All Critical & High Priority Features Delivered*
