from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from analytics import analyze_text

app = FastAPI()

# allow React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = "data/RateMyProfessor_Sample.csv"
df = pd.read_csv(DATA_PATH)

df = df[['professor_name','department_name','star_rating','student_difficult','comments']].dropna()
df = df.rename(columns={
    "department_name": "course",
    "star_rating": "quality",
    "student_difficult": "difficulty"
})

# ========= ALL PROFESSORS =========
@app.get("/professors")
def get_professors():
    profs = df["professor_name"].unique().tolist()
    return profs

# ========= PROFESSOR DATA =========
@app.get("/professor/{name}")
def professor_detail(name: str):
    pdf = df[df["professor_name"] == name]

    avg_rating = round(pdf["quality"].mean(),2)
    avg_diff = round(pdf["difficulty"].mean(),2)

    sentiments = []
    categories = []

    for c in pdf["comments"].sample(min(50, len(pdf))):
        s, cat = analyze_text(c)
        sentiments.append(s)
        categories.extend(cat)

    return {
        "professor": name,
        "courses": pdf["course"].unique().tolist(),
        "avg_rating": avg_rating,
        "avg_difficulty": avg_diff,
        "sentiment_counts": pd.Series(sentiments).value_counts().to_dict(),
        "category_counts": pd.Series(categories).value_counts().to_dict()
    }

# ========= SEARCH =========
@app.get("/search")
def search_prof(q: str):
    q = q.lower()
    matches = [p for p in df["professor_name"].unique() if q in p.lower()]
    return matches
