from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
from analytics import analyze_text
from trend_analysis import (
    analyze_rating_trend,
    predict_future_rating,
    compare_professors,
    get_top_professors
)

app = FastAPI(title="Course & Instructor Evaluation Analytics API")

# allow React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000", "https://nlp-project953482.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
DATA_PATH = "data/RateMyProfessor_Sample.csv"
df_raw = pd.read_csv(DATA_PATH)

# Select and rename columns - เพิ่มคอลัมน์ใหม่สำหรับวิชา
df = df_raw[[
    'professor_name',
    'department_name',
    'name_not_onlines',    # เพิ่ม - รหัสวิชา (ใช้ name_not_onlines ไม่ใช่ local_name)
    'IsCourseOnline',       # เพิ่ม - ประเภทวิชา
    'student_star',
    'student_difficult',
    'comments',
    'post_date'
]].dropna()

df = df.rename(columns={
    "department_name": "course",          # เปลี่ยนชื่อให้สื่อความหมายมากขึ้น
    "name_not_onlines": "course_code",    # เพิ่ม - รหัสวิชา (ใช้ name_not_onlines)
    "IsCourseOnline": "course_type",      # เพิ่ม - ประเภท (0/1)
    "student_star": "quality",
    "student_difficult": "difficulty",
    "post_date": "date"
})
df['date'] = pd.to_datetime(df['date'])

# แปลงค่า 0/1 เป็น "onsite"/"online"
df['course_type'] = df['course_type'].map({0: 'onsite', 1: 'online'})

# Handle "NAN" string values in course_code
df['course_code'] = df['course_code'].replace('NAN', None)
df['course_code'] = df['course_code'].fillna('N/A')

# ========= SUBJECT DATA =========
def get_all_subjects(df):
    """สร้างรายการวิชาทั้งหมดพร้อมสถิติ"""
    subjects = {}

    for _, row in df.iterrows():
        course_name = row['course']
        # ใช้ course_code จาก name_not_onlines (ถ้ามีค่า "NAN" ให้ใช้ค่าว่าง)
        course_code = row.get('course_code', 'N/A')
        if pd.isna(course_code) or course_code == 'NAN':
            course_code = 'N/A'
        course_type = row.get('course_type', 'unknown')

        key = f"{course_name}|{course_type}"

        if key not in subjects:
            subjects[key] = {
                'name': course_name,
                'code': course_code,
                'type': course_type,
                'count': 0,
                'avg_quality': 0,
                'avg_difficulty': 0,
                'professors': set(),
                'course_codes': set()  # เก็บรหัสวิชาทั้งหมด
            }

        subjects[key]['count'] += 1
        subjects[key]['professors'].add(row['professor_name'])
        subjects[key]['course_codes'].add(course_code)

    # คำนวณค่าเฉลี่ย
    for key in subjects:
        subject_df = df[
            (df['course'] == subjects[key]['name']) &
            (df['course_type'] == subjects[key]['type'])
        ]
        subjects[key]['avg_quality'] = round(subject_df['quality'].mean(), 2)
        subjects[key]['avg_difficulty'] = round(subject_df['difficulty'].mean(), 2)
        subjects[key]['professor_count'] = len(subjects[key]['professors'])
        subjects[key]['professors'] = list(subjects[key]['professors'])[:5]  # โชว์ 5 คนแรก
        subjects[key]['course_codes'] = list(subjects[key]['course_codes'])[:10]  # โชว์ 10 รหัสแรก

    # Convert to list and filter by minimum review count
    subjects_list = list(subjects.values())
    subjects_list = [s for s in subjects_list if s['count'] >= 5]  # เฉพาะวิชาที่มี >= 5 รีวิว

    return subjects_list

# เรียกใช้ตอนเริ่ม
all_subjects = get_all_subjects(df)

# ========= ALL PROFESSORS =========
@app.get("/professors")
def get_professors():
    """Get list of all professor names"""
    profs = df["professor_name"].unique().tolist()
    return profs

# ========= PROFESSOR DATA =========
@app.get("/professor/{name}")
def professor_detail(name: str):
    """Get detailed analytics for a specific professor"""
    pdf = df[df["professor_name"] == name]

    if len(pdf) == 0:
        raise HTTPException(status_code=404, detail=f"Professor '{name}' not found")

    avg_rating = round(pdf["quality"].mean(), 2)
    avg_diff = round(pdf["difficulty"].mean(), 2)
    num_ratings = len(pdf)

    sentiments = []
    categories = []

    # Sample up to 50 comments for analysis
    sample_comments = pdf["comments"].sample(min(50, len(pdf))) if len(pdf) > 50 else pdf["comments"]

    for c in sample_comments:
        s, cat, _ = analyze_text(c) 
        sentiments.append(s)
        categories.extend(cat)

    # Calculate sentiment percentages
    sentiment_counts = pd.Series(sentiments).value_counts()
    sentiment_percentages = {
        k: round(v / len(sentiments) * 100, 1) for k, v in sentiment_counts.to_dict().items()
    }

    # Category counts
    category_counts = pd.Series(categories).value_counts().to_dict()

    return {
        "professor": name,
        "courses": pdf["course"].unique().tolist(),
        "avg_rating": avg_rating,
        "avg_difficulty": avg_diff,
        "num_ratings": num_ratings,
        "sentiment_counts": sentiment_counts.to_dict(),
        "sentiment_percentages": sentiment_percentages,
        "category_counts": category_counts
    }

# ========= SEARCH =========
@app.get("/search")
def search_prof(q: str):
    """Search professors by name"""
    q = q.lower()
    matches = [p for p in df["professor_name"].unique() if q in p.lower()]
    return matches

# ========= TREND ANALYSIS =========
@app.get("/professor/{name}/trend")
def get_professor_trend(name: str):
    """Get rating trend analysis for a professor"""
    result = analyze_rating_trend(name, df)

    if "error" in result:
        if "not found" in result["error"].lower():
            raise HTTPException(status_code=404, detail=result["error"])

    return result

# ========= PREDICTION =========
@app.get("/professor/{name}/predict")
def predict_professor_rating(name: str, periods: int = 5):
    """Predict future ratings for a professor using linear regression"""
    if periods < 1 or periods > 20:
        raise HTTPException(status_code=400, detail="Periods must be between 1 and 20")

    result = predict_future_rating(name, periods, df)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result

# ========= COMPARE PROFESSORS =========
class CompareRequest(BaseModel):
    professors: List[str]

@app.post("/professors/compare")
def compare_professors_endpoint(request: CompareRequest):
    """Compare multiple professors"""
    result = compare_professors(request.professors, df)

    if result["total_professors"] == 0:
        raise HTTPException(status_code=404, detail="No valid professors found")

    return result

# Alternative: GET endpoint for comparison
@app.get("/professors/compare")
def compare_professors_get(names: str):
    """Compare multiple professors (comma-separated names)"""
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
    """Get top N professors by various criteria"""
    valid_criteria = ["rating", "difficulty", "easiest", "hardest", "most_reviews", "most_consistent","predicted"]

    if by not in valid_criteria:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid criteria. Must be one of: {', '.join(valid_criteria)}"
        )

    if n < 1 or n > 50:
        raise HTTPException(status_code=400, detail="n must be between 1 and 50")

    return get_top_professors(by, n, min_ratings, df)

# ========= TOP PREDICTION VIEW =========
@app.get("/professors/predicted-rankings")
def predicted_rankings(n: int = 10, min_ratings: int = 5):
    from trend_analysis import get_predicted_rankings
    return get_predicted_rankings(n, min_ratings, df)


# ========= SUBJECTS =========
@app.get("/subjects")
def get_subjects(
    type: Optional[str] = None,  # "online" หรือ "onsite" หรือ None (ทั้งหมด)
    search: Optional[str] = None  # ค้นหาชื่อวิชา
):
    """ดึงรายการวิชาทั้งหมด กรองตามประเภทและชื่อ"""
    subjects = all_subjects.copy()

    if type:
        subjects = [s for s in subjects if s['type'] == type]

    if search:
        search_lower = search.lower()
        subjects = [s for s in subjects if search_lower in s['name'].lower()]

    return {
        "total": len(subjects),
        "subjects": subjects
    }

@app.get("/subject/{name}")
def get_subject_detail(name: str, type: str):
    """ดึงข้อมูลละเอียดของวิชาตามชื่อและประเภท"""
    subject_df = df[
        (df['course'] == name) &
        (df['course_type'] == type)
    ]

    if len(subject_df) == 0:
        raise HTTPException(status_code=404, detail="Subject not found")

    # NLP Analysis สำหรับวิชา
    comments = subject_df["comments"].sample(min(50, len(subject_df)))
    sentiments = []
    categories = []

    for c in comments:
        s, cat, _ = analyze_text(c)
        sentiments.append(s)
        categories.extend(cat)

    # Get top professors in this subject
    top_profs = subject_df.groupby('professor_name')['quality'].mean().nlargest(5).to_dict()

    return {
        "name": name,
        "type": type,
        "avg_quality": round(subject_df['quality'].mean(), 2),
        "avg_difficulty": round(subject_df['difficulty'].mean(), 2),
        "total_reviews": len(subject_df),
        "professor_count": subject_df['professor_name'].nunique(),
        "top_professors": top_profs,
        "sentiment_distribution": pd.Series(sentiments).value_counts().to_dict(),
        "category_counts": pd.Series(categories).value_counts().to_dict(),
        "course_codes": subject_df['course_code'].unique().tolist()[:10]
    }

@app.get("/professor/{name}/subjects")
def get_professor_subjects(name: str):
    """ดึงรายการวิชาที่อาจารย์สอน แยกตามประเภท"""
    prof_df = df[df['professor_name'] == name]

    if len(prof_df) == 0:
        raise HTTPException(status_code=404, detail="Professor not found")

    subjects = []
    for (course, course_type), group in prof_df.groupby(['course', 'course_type']):
        subjects.append({
            'name': course,
            'type': course_type,
            'avg_quality': round(group['quality'].mean(), 2),
            'avg_difficulty': round(group['difficulty'].mean(), 2),
            'review_count': len(group)
        })

    return {
        "professor": name,
        "subjects": subjects
    }

# ========= HEALTH CHECK =========
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "total_professors": df["professor_name"].nunique(),
        "total_ratings": len(df),
        "datasets": ["RateMyProfessor"],
        "endpoints": {
            "professors": "/professors",
            "professor_detail": "/professor/{name}",
            "professor_trend": "/professor/{name}/trend",
            "professor_predict": "/professor/{name}/predict",
            "search": "/search?q=query",
            "compare": "/professors/compare",
            "top": "/professors/top",
            "subjects": "/subjects",
            "subject_detail": "/subject/{name}?type=online|onsite",
            "professor_subjects": "/professor/{name}/subjects"
        }
    }

# ========= ROOT =========
@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "name": "Course & Instructor Evaluation Analytics API",
        "version": "1.0.0",
        "description": "NLP-powered sentiment analysis, trend prediction, and multi-label categorization",
        "endpoints": {
            "professors": "/professors",
            "professor_detail": "/professor/{name}",
            "professor_trend": "/professor/{name}/trend",
            "professor_predict": "/professor/{name}/predict?periods=5",
            "search": "/search?q=query",
            "compare": "/professors/compare?names=prof1,prof2",
            "top": "/professors/top?by=rating&n=10",
            "subjects": "/subjects?type=online|onsite&search=query",
            "subject_detail": "/subject/{name}?type=online|onsite",
            "professor_subjects": "/professor/{name}/subjects"
        }
    }
