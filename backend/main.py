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
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
DATA_PATH = "data/RateMyProfessor_Sample.csv"
df_raw = pd.read_csv(DATA_PATH)

# Select and rename columns
df = df_raw[['professor_name','department_name','star_rating','student_difficult','comments']].dropna()
df = df.rename(columns={
    "department_name": "course",
    "star_rating": "quality",
    "student_difficult": "difficulty"
})

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
    valid_criteria = ["rating", "difficulty", "easiest", "hardest", "most_reviews", "most_consistent"]

    if by not in valid_criteria:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid criteria. Must be one of: {', '.join(valid_criteria)}"
        )

    if n < 1 or n > 50:
        raise HTTPException(status_code=400, detail="n must be between 1 and 50")

    return get_top_professors(by, n, min_ratings, df)

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
            "top": "/professors/top"
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
            "top": "/professors/top?by=rating&n=10"
        }
    }
