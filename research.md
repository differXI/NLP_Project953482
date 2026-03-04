# NLP-953482: Course & Instructor Evaluation Analytics System

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
10. [System Capabilities](#system-capabilities)
11. [Known Limitations](#known-limitations)
12. [Next Steps](#next-steps)

---

## Problem Statement

### Four Key Challenges:

1. **Limited Interpretability of Numerical Scores**
   - Numerical ratings summarize satisfaction but lack contextual explanations
   - Cannot identify specific causes behind evaluation results
   - Rating alone doesn't indicate what needs improvement

2. **Manual Analysis of Textual Feedback**
   - Time-consuming and labor-intensive process
   - Difficult to standardize across multiple reviewers
   - Inconsistent analysis due to human subjectivity
   - Not scalable for large volumes of feedback

3. **Lack of Structured Categorization**
   - Existing systems focus only on overall sentiment (positive/negative)
   - Cannot identify specific aspects of teaching performance systematically
   - No way to group feedback by meaningful categories

4. **Inconsistent Interpretation**
   - Manual interpretation introduces subjectivity
   - Different evaluators may interpret the same comment differently
   - Reduces reliability and fairness of evaluation

---

## System Objectives

The system aims to achieve the following objectives:

1. ✅ **Analyze structured evaluation data** using standard statistical methods
2. ✅ **Classify open-ended textual feedback** into positive, negative, and neutral sentiment
3. ✅ **Detect and categorize multiple issues** within a single comment
4. ✅ **Organize feedback into meaningful subcategories** for deeper analysis
5. ❌ **Predict future instructor and course popularity trends** based on historical data (NOT YET IMPLEMENTED)

---

## Methodology

### 1. Quantitative Data Analysis

Focuses on structured evaluation data:
- Rating-scale questions (1-5 scale)
- Multiple-choice or fixed-answer questions

**Current Analysis Techniques:**
- ✅ Descriptive statistics (mean, distribution, frequency)
- ✅ Basic comparative analysis
- ❌ Trend and Time-Series Analysis (NOT IMPLEMENTED)
- ❌ Linear Regression for forecasting (NOT IMPLEMENTED)

### 2. NLP-Based Qualitative Text Analysis

#### AI Techniques Used:

**2.1 Supervised Learning**
- Sentiment classification (Positive / Negative / Neutral)
- Multi-label subcategory classification
- **Current Models:** Pre-trained models using scikit-learn

**2.2 Feature Representation**
- ✅ TF-IDF vectorization (current implementation)
- ⚠️ Word embeddings (not implemented)

**2.3 Model Architecture**
- **Vectorization:** TfidfVectorizer
- **Sentiment Model:** Logistic Regression / Multiclass classifier
- **Category Model:** Multi-label classifier with MultiLabelBinarizer

#### Sentiment Classification
- **Type:** Multi-class classification
- **Labels:** Positive, Negative, Neutral
- **Current Model:** Logistic Regression (pre-trained)
- **Status:** Model exists but NO training script available

#### Multi-Issue Detection
- Identifies multiple opinions/concerns within a single comment
- Example: Comment may mention both teaching clarity AND speaking pace issues
- Handled by multi-label classification approach

#### Subcategory Classification (5 Categories)

| Category | Description | Examples |
|----------|-------------|----------|
| **Teaching Clarity** | Explanation quality, examples, logical flow | "clear explanations", "confusing lectures", "easy to understand" |
| **Speaking Pace** | Delivery speed, verbal presentation, vocal clarity | "too fast", "clear voice", "appropriate pace", "mumbles" |
| **Course Structure** | Organization, syllabus, assignments, workload | "well organized", "disorganized", "heavy workload", "structured" |
| **Communication** | Responsiveness, feedback, answering questions | "helpful", "unresponsive", "available", "ignores questions" |
| **Professional Behavior** | Punctuality, fairness, respect, ethics | "professional", "rude", "fair grading", "respectful" |

---

## Technical Architecture

### Backend (Python + FastAPI)

**Directory Structure:**
```
backend/
├── main.py              # FastAPI application & API endpoints (64 lines)
├── analytics.py         # NLP analysis functions (13 lines)
├── requirements.txt     # Python dependencies
├── data/                # Dataset storage
│   └── RateMyProfessor_Sample.csv  # Main dataset (10.8MB)
└── models/              # Pre-trained ML models
    ├── vectorizer.pkl   # TF-IDF vectorizer (197KB)
    ├── sentiment_model.pkl  # Sentiment classifier (121KB)
    ├── category_model.pkl   # Category classifier (283KB)
    └── mlb.pkl          # MultiLabelBinarizer (602 bytes)
```

**File Descriptions:**

**[main.py](backend/main.py)** (64 lines)
- FastAPI application with CORS support
- Data loading from RateMyProfessor dataset
- Three main API endpoints:
  - `GET /professors` - List all professor names
  - `GET /professor/{name}` - Get detailed analytics for a professor
  - `GET /search` - Search professors by name
- Data processing:
  - Loads CSV data
  - Renames columns (department_name→course, star_rating→quality, student_difficult→difficulty)
  - Samples up to 50 comments per professor for NLP analysis
  - Calculates average ratings and sentiment/category counts

**[analytics.py](backend/analytics.py)** (13 lines)
- Loads pre-trained models from `models/` directory
- `analyze_text(text: str)` function:
  - Input: Raw comment text
  - Output: (sentiment_label, [category_list])
  - Uses TF-IDF vectorization
  - Predicts sentiment (positive/negative/neutral)
  - Predicts categories (multi-label)

### Frontend (React)

**Directory Structure:**
```
frontend/
├── src/
│   ├── App.jsx                    # Main application component (38 lines)
│   ├── api.js                     # API client functions (8 lines)
│   ├── index.js                   # React entry point
│   └── components/
│       ├── SearchBar.jsx          # Search functionality (17 lines)
│       ├── ProfessorList.jsx      # List of professors (12 lines)
│       ├── ProfessorCard.jsx      # Individual professor card (16 lines)
│       └── Insights.jsx           # Analytics dashboard (33 lines)
└── package.json                   # Node dependencies (React 19.2.4, Recharts 3.7.0)
```

**File Descriptions:**

**[App.jsx](frontend/src/App.jsx)** (38 lines)
- Main React application component
- State management:
  - `profs` - List of all professors
  - `selected` - Currently selected professor name
  - `data` - Analytics data for selected professor
- Functions:
  - `selectProf(name)` - Fetches and displays professor analytics
  - `search(q)` - Filters professor list by search query
- Layout: Simple inline-styled UI with search, list, and insights

**[api.js](frontend/src/api.js)** (8 lines)
- Axios-based HTTP client
- Base URL: `http://127.0.0.1:8000`
- Functions:
  - `getProfessors()` - Get all professor names
  - `getProfessor(name)` - Get professor details
  - `searchProf(q)` - Search professors

**[Insights.jsx](frontend/src/components/Insights.jsx)** (33 lines)
- Displays analytics for selected professor
- Shows:
  - Professor name
  - Average rating
  - Average difficulty
  - Sentiment distribution bar chart
  - Category breakdown bar chart
- Uses Recharts library for visualization

**[SearchBar.jsx](frontend/src/components/SearchBar.jsx)** (17 lines)
- Simple search input component
- Controlled input with search button

**[ProfessorList.jsx](frontend/src/components/ProfessorList.jsx)** (12 lines)
- Renders list of ProfessorCard components
- Maps over professor array

**[ProfessorCard.jsx](frontend/src/components/ProfessorCard.jsx)** (16 lines)
- Clickable card for each professor
- Triggers onSelect callback when clicked

### API Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/professors` | GET | Get all professor names | ✅ Working |
| `/professor/{name}` | GET | Get detailed analytics for a professor | ✅ Working |
| `/search?q=query` | GET | Search professors by name | ✅ Working |

---

## Current Implementation Status

### ✅ What Currently Works

1. **Backend API**
   - ✅ FastAPI server runs on port 8000
   - ✅ CORS enabled for React frontend
   - ✅ Data loading from CSV (10.8MB dataset)
   - ✅ Three basic endpoints operational

2. **NLP Analysis**
   - ✅ Pre-trained models loaded successfully
   - ✅ Sentiment prediction (positive/negative/neutral)
   - ✅ Multi-label category classification (5 categories)
   - ✅ TF-IDF vectorization
   - ✅ Samples up to 50 comments per professor

3. **Frontend**
   - ✅ React application (Create React App)
   - ✅ Professor listing
   - ✅ Search functionality
   - ✅ Professor detail view
   - ✅ Analytics dashboard with charts

### ❌ Critical Missing Components

**🔴 CRITICAL GAP: Training Scripts Do NOT Exist**

The project has pre-trained model files (`.pkl`) but lacks:
- ❌ **Training script for Sentiment Classification** (`train_sentiment.py`)
- ❌ **Training script for Category Classification** (`train_categories.py`)
- ❌ **Complete training pipeline** (`train_all.py`)
- ❌ **Model evaluation script** (`evaluate_models.py`)
- ❌ **Documentation on model training process**

**Impact:**
- Models cannot be retrained with new data
- No reproducibility of model creation
- Cannot update models with additional datasets (Coursera)
- Training methodology is undocumented
- No evaluation metrics (accuracy, precision, recall, F1)

### ❌ Missing Features (from Project Proposal)

1. **No Trend Analysis**
   - ❌ Cannot analyze rating trends over time
   - ❌ Cannot predict future ratings
   - ❌ No time-series visualization
   - ❌ Missing Linear Regression implementation

2. **No Comparison Features**
   - ❌ Cannot compare multiple professors
   - ❌ No ranking or top professors view
   - ❌ No side-by-side analytics

3. **No Data Integration**
   - ❌ Using only RateMyProfessor data
   - ❌ Cannot integrate Coursera dataset
   - ❌ No combined dataset functionality

4. **Limited Frontend**
   - ❌ Basic UI only
   - ❌ No view toggle (individual vs comparison)
   - ❌ No trend charts
   - ❌ No prediction displays

---

## Proposed Features

Based on the project proposal, the following features should be implemented:

### Phase 1: Model Training Infrastructure (🔴 CRITICAL - Missing)
- **Required Files:**
  - `backend/train_sentiment.py` - Train sentiment classifier
  - `backend/train_categories.py` - Train multi-label category classifier
  - `backend/train_all.py` - Complete training pipeline
  - `backend/evaluate_models.py` - Model testing and evaluation
- **Benefits:**
  - Enable model retraining
  - Provide reproducibility
  - Allow integration of new datasets
  - Track model performance metrics

### Phase 2: Trend Analysis & Prediction (🔴 HIGH PRIORITY - Missing)
- **Required Files:**
  - `backend/trend_analysis.py` - Linear regression trend analysis
  - `frontend/src/components/TrendChart.jsx` - Trend visualization
- **API Endpoints:**
  - `GET /professor/{name}/trend` - Historical trend data
  - `GET /professor/{name}/predict?periods=5` - Future predictions
- **Features:**
  - Time-series rating analysis
  - Linear regression forecasting
  - Trend direction indicators
  - Confidence intervals

### Phase 3: Comparison Features (🟡 MEDIUM PRIORITY - Missing)
- **Required Files:**
  - `frontend/src/components/ComparisonDashboard.jsx` - Comparison UI
- **API Endpoints:**
  - `GET /professors/compare?names=prof1,prof2` - Compare multiple professors
  - `GET /professors/top?by=rating&n=10` - Top N professors
- **Features:**
  - Side-by-side professor comparison
  - Ranking by various criteria
  - Multi-dimensional radar charts
  - Grouped bar charts

### Phase 4: Data Integration (🟡 MEDIUM PRIORITY - Missing)
- **Required Files:**
  - `backend/data_loader.py` - Coursera dataset integration
- **Features:**
  - Load and normalize Coursera dataset
  - Combine with RateMyProfessor data
  - Expanded training data
  - Improved model accuracy

---

## Development Milestones

### Phase 1: Requirement Analysis and Data Preparation ✅ COMPLETE
- [x] Review evaluation system requirements
- [x] Define analytical categories (5 subcategories)
- [x] Prepare datasets (RateMyProfessor loaded)
- [ ] ⚠️ Coursera dataset integration (pending)

### Phase 2: Quantitative Data Analysis Module ⚠️ PARTIAL
- [x] Descriptive statistics (mean, distribution)
- [x] Basic comparative analysis
- [ ] ❌ Trend and Time-Series Analysis (NOT IMPLEMENTED)
- [ ] ❌ Linear Regression for forecasting (NOT IMPLEMENTED)

### Phase 3: NLP Model Development ⚠️ PARTIAL
- [x] Pre-trained models exist
- [ ] ❌ Training scripts MISSING
- [ ] ❌ Model evaluation MISSING
- [ ] ❌ Reproducibility NOT POSSIBLE

### Phase 4: System Integration and Testing ⚠️ PARTIAL
- [x] Basic frontend-backend integration
- [x] API endpoints operational
- [ ] ❌ Trend endpoints MISSING
- [ ] ❌ Comparison endpoints MISSING
- [ ] ⚠️ Limited testing

### Phase 5: Result Analysis and Documentation ⚠️ PARTIAL
- [x] Basic visualization of results
- [ ] ❌ Advanced analytics dashboard
- [ ] ❌ Trend visualization
- [ ] ⚠️ Documentation incomplete

---

## Datasets

### Current Dataset: RateMyProfessor Sample

**File:** `backend/data/RateMyProfessor_Sample.csv`
**Size:** ~10.8MB
**Records:** ~100K+ professor reviews

**Columns:**
- `professor_name` - Name of the instructor
- `department_name` → renamed to `course` - Course/department
- `star_rating` → renamed to `quality` - 1-5 rating scale
- `student_difficult` → renamed to `difficulty` - 1-5 difficulty scale
- `comments` - Student feedback text (used for NLP analysis)

**Data Processing:**
- Columns renamed for consistency
- Rows with missing values dropped
- Up to 50 comments sampled per professor for NLP analysis

### Optional Dataset: Coursera Reviews (NOT INTEGRATED)

**File:** Would be `backend/data/Coursera_reviews.csv`
**Size:** 100K reviews
**Status:** Not integrated yet
**Purpose:** Additional training data for improved model accuracy

---

## Technology Stack

### Backend

| Technology | Purpose |
|------------|---------|
| **Python** | Core language |
| **FastAPI** | Web framework for API |
| **pandas** | Data manipulation and analysis |
| **scikit-learn** | ML models and vectorization |
| **joblib** | Model persistence |
| **numpy** | Numerical computing |

**Dependencies:** See [backend/requirements.txt](backend/requirements.txt)

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 19.2.4 | UI framework |
| **Create React App** | 5.0.1 | Build tool |
| **Recharts** | 3.7.0 | Data visualization |
| **Axios** | 1.13.6 | HTTP client |

**Dependencies:** See [frontend/package.json](frontend/package.json)

---

## System Capabilities

### What the System Can Do NOW

1. **List Professors**
   - Displays all unique professor names from dataset
   - API: `GET /professors`

2. **Search Professors**
   - Filter professors by name (case-insensitive)
   - API: `GET /search?q=query`

3. **View Professor Analytics**
   - Average quality rating (1-5 scale)
   - Average difficulty rating (1-5 scale)
   - List of courses taught
   - Sentiment distribution (positive/negative/neutral counts)
   - Category breakdown (5 subcategories with mention counts)
   - API: `GET /professor/{name}`

4. **Analyze Comments**
   - Classify sentiment using pre-trained model
   - Classify categories using multi-label model
   - Sample up to 50 comments per professor
   - Uses TF-IDF + Logistic Regression

### What the System CANNOT Do YET

1. **No Trend Analysis**
   - Cannot see how ratings change over time
   - Cannot identify upward/downward trends
   - Cannot analyze temporal patterns

2. **No Prediction**
   - Cannot forecast future ratings
   - Cannot predict instructor popularity
   - Cannot estimate future performance

3. **No Comparison**
   - Cannot compare multiple professors
   - Cannot rank or find top professors
   - Cannot side-by-side analytics

4. **No Retraining**
   - Cannot retrain models with new data
   - Cannot integrate Coursera dataset
   - Cannot improve model accuracy
   - Cannot evaluate model performance

5. **No Advanced Visualization**
   - No trend charts
   - No prediction displays
   - No comparison dashboards
   - No radar charts or multi-dimensional plots

---

## Known Limitations

### 🔴 Critical Technical Limitations

1. **Missing Training Infrastructure**
   - **Issue:** No way to retrain or update models
   - **Impact:** Cannot adapt to new data or improve accuracy
   - **Severity:** CRITICAL - Blocks all model improvements
   - **Fix Required:** Create training scripts (train_sentiment.py, train_categories.py, train_all.py)

2. **No Trend Analysis**
   - **Issue:** Cannot analyze temporal patterns
   - **Impact:** Cannot identify changes in performance over time
   - **Severity:** HIGH - Core project requirement not met
   - **Fix Required:** Implement trend_analysis.py with Linear Regression

3. **No Prediction Capability**
   - **Issue:** Cannot forecast future performance
   - **Impact:** Cannot meet project objective #5
   - **Severity:** HIGH - Explicit project requirement
   - **Fix Required:** Add prediction endpoints and visualization

### 🟡 Medium Data Limitations

4. **Single Data Source**
   - **Issue:** Only RateMyProfessor data
   - **Impact:** Limited training diversity
   - **Severity:** MEDIUM - Coursera integration would help
   - **Fix Required:** Create data_loader.py

5. **No Date Field**
   - **Issue:** No temporal information in dataset
   - **Impact:** Cannot do trend analysis without synthetic data
   - **Severity:** MEDIUM - Can work around with synthetic dates
   - **Fix Required:** Add date generation or use alternative data

### 🟢 Lower Model Limitations

6. **Unknown Model Performance**
   - **Issue:** No evaluation metrics available
   - **Impact:** Don't know accuracy, precision, recall, F1
   - **Severity:** MEDIUM - Cannot assess quality
   - **Fix Required:** Create evaluate_models.py

7. **Limited Context Understanding**
   - **Issue:** May struggle with sarcasm, irony
   - **Impact:** Misclassification of nuanced comments
   - **Severity:** LOW - Common NLP limitation
   - **Potential Fix:** BERT fine-tuning (optional)

### 🟢 Infrastructure Limitations

8. **No Reproducibility**
   - **Issue:** Cannot reproduce model training
   - **Impact:** Cannot verify or improve models
   - **Severity:** HIGH - Academic/research requirement
   - **Fix Required:** Training scripts with documentation

9. **No Scalability**
   - **Issue:** Sampling only 50 comments
   - **Impact:** May miss important feedback
   - **Severity:** LOW - Performance trade-off
   - **Potential Fix:** Configurable sampling or full analysis

---

## How the System Currently Works

### Backend Flow

```
1. Load CSV data (RateMyProfessor_Sample.csv - 10.8MB)
   ↓
2. Rename & clean columns
   - department_name → course
   - star_rating → quality
   - student_difficult → difficulty
   ↓
3. API request received (e.g., GET /professor/{name})
   ↓
4. Filter data for requested professor
   ↓
5. Sample up to 50 comments (random sampling)
   ↓
6. For each comment:
   - Vectorize with pre-trained TF-IDF vectorizer
   - Predict sentiment (positive/negative/neutral)
   - Predict categories (multi-label, up to 5)
   ↓
7. Aggregate results:
   - Count sentiments
   - Count categories
   - Calculate averages
   ↓
8. Return JSON response
```

### Frontend Flow

```
1. User searches for professor
   ↓
2. SearchBar.jsx calls onSearch(q)
   ↓
3. App.jsx calls searchProf(q)
   ↓
4. API call to GET /search?q=query
   ↓
5. Professor list updates with filtered results
   ↓
6. User selects professor from list
   ↓
7. ProfessorCard.jsx triggers onSelect(prof)
   ↓
8. App.jsx calls selectProf(name)
   ↓
9. API call to GET /professor/{name}
   ↓
10. Receive analytics data:
    - avg_rating
    - avg_difficulty
    - courses
    - sentiment_counts
    - category_counts
    ↓
11. Insights.jsx renders:
    - Professor info
    - Rating stats
    - Sentiment chart (Recharts BarChart)
    - Category chart (Recharts BarChart)
```

---

## Next Steps

To complete the project according to the proposal, tasks are prioritized as follows:

### 🔴 CRITICAL Priority (Must Complete)

1. **Create NLP Model Training Scripts**
   - `backend/train_sentiment.py` - Train sentiment classifier
   - `backend/train_categories.py` - Train category classifier
   - `backend/train_all.py` - Complete pipeline
   - `backend/evaluate_models.py` - Testing framework
   - **Why:** Cannot retrain, reproduce, or improve models without these
   - **Impact:** Enables all future model improvements

2. **Implement Trend Analysis**
   - `backend/trend_analysis.py` - Linear regression
   - Add synthetic date generation
   - Create trend endpoints
   - **Why:** Core project requirement (Objective #5)
   - **Impact:** Enables prediction feature

### 🔴 HIGH Priority (Should Complete)

3. **Add Prediction Capability**
   - Future rating prediction endpoint
   - `frontend/src/components/TrendChart.jsx`
   - Confidence intervals
   - **Why:** Completes Objective #5
   - **Impact:** Full requirements compliance

4. **Model Evaluation Framework**
   - Accuracy, precision, recall, F1-score
   - Confusion matrices
   - **Why:** Cannot assess model quality
   - **Impact:** Validated research results

### 🟡 MEDIUM Priority (Nice to Have)

5. **Comparison Features**
   - Professor comparison dashboard
   - Top professors ranking
   - **Why:** Enhanced analytics
   - **Impact:** Better insights for users

6. **Data Integration**
   - Coursera dataset loader
   - Combined dataset
   - **Why:** Improved training data
   - **Impact:** Better model accuracy

### 🟢 LOW Priority (Optional)

7. **UI/UX Improvements**
   - Enhanced visualizations
   - Better dashboards
   - **Why:** User experience
   - **Impact:** More polished application

8. **BERT Fine-tuning**
   - Advanced NLP model
   - Better context understanding
   - **Why:** Improved accuracy
   - **Impact:** State-of-the-art performance

---

## Summary

**Current State:** A working NLP-powered evaluation analytics system with basic sentiment analysis and categorization capabilities. The system successfully classifies feedback into 5 categories but lacks critical training infrastructure, trend analysis, and prediction features.

**Critical Gap:** No training scripts exist, making model reproduction and improvement impossible.

**Path Forward:** Prioritize creating training scripts and implementing trend analysis to meet all project requirements.

---

*Last Updated: March 4, 2026*
*Project Status: Phase 3 (NLP Model Development) - Partially Complete*
*Critical Gap: Training Scripts Missing*
