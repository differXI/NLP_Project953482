"""
Trend Analysis and Prediction Module

Provides functions for:
- Analyzing rating trends over time
- Predicting future ratings using Linear Regression
- Comparing multiple professors
- Finding top professors by various criteria
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from typing import Dict, List, Optional

def add_synthetic_dates(df):
    """
    สร้างคอลัมน์วันที่จำลอง โดย 'เรียงตามลำดับข้อมูล' (Sequential)
    เพื่อรักษาเค้าโครงของ Trend เดิมไว้ (ดีกว่าการสุ่มมั่วๆ)
    """
    if 'post_date' in df.columns:
        return df

    df = df.copy()
    n_samples = len(df)
    
    end_date = datetime(2024, 1, 1)
    start_date = end_date - timedelta(days=730) 
    
    date_range = pd.date_range(start=start_date, end=end_date, periods=n_samples)
    df['post_date'] = date_range

    return df


def analyze_rating_trend(professor_name: str, df):
    """Analyze rating trend for a specific professor"""
    pdf = df[df['professor_name'] == professor_name]

    if len(pdf) == 0:
        return {
            "error": f"Professor '{professor_name}' not found",
            "available_professors": df['professor_name'].unique().tolist()[:10]
        }

    #pdf = add_synthetic_dates(pdf)
    
    pdf['year_month'] = pd.to_datetime(pdf['date']).dt.to_period('M')

    monthly_data = pdf.groupby('year_month').agg({
        'quality': ['mean', 'count']
    }).reset_index()

    monthly_data.columns = ['year_month', 'avg_rating', 'num_ratings']

    if len(monthly_data) < 3:
        return {
            "error": f"Not enough data points for '{professor_name}'. Only {len(monthly_data)} months of data.",
            "min_months_required": 3
        }

    monthly_data = monthly_data.sort_values('year_month')
    monthly_data['year_month'] = monthly_data['year_month'].astype(str)

    # เตรียมข้อมูลทำ Linear Regression
    X = np.arange(len(monthly_data)).reshape(-1, 1)
    y = monthly_data['avg_rating'].values

    model = LinearRegression()
    model.fit(X, y)
    trend_line = model.predict(X)

    # คำนวณความน่าเชื่อถือ (R-squared)
    y_mean = np.mean(y)
    ss_tot = np.sum((y - y_mean) ** 2)
    ss_res = np.sum((y - trend_line) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    # ดูทิศทางของกราฟ (ขึ้น/ลง)
    slope = model.coef_[0]
    if slope > 0.05:
        trend_direction = "increasing"
    elif slope < -0.05:
        trend_direction = "decreasing"
    else:
        trend_direction = "stable"

    # คำนวณ % การเปลี่ยนแปลง (จากเดือนแรก -> เดือนสุดท้าย)
    if len(y) >= 2:
        first_avg = y[0]
        last_avg = y[-1]
        trend_percentage = ((last_avg - first_avg) / first_avg) * 100
    else:
        trend_percentage = 0

    return {
        "professor": professor_name,
        "dates": monthly_data['year_month'].tolist(),
        "ratings": np.round(monthly_data['avg_rating'], 2).tolist(), # ปัดเศษ 2 ตำแหน่ง
        "num_ratings_per_month": monthly_data['num_ratings'].tolist(),
        "trend_line": np.round(trend_line, 2).tolist(), # ปัดเศษ 2 ตำแหน่ง
        "trend_direction": trend_direction,
        "trend_percentage": round(trend_percentage, 2),
        "model_quality": {
            "r_squared": round(r_squared, 3),
            "slope": round(slope, 4)
        },
        "data_points": len(monthly_data)
    }


def predict_future_rating(professor_name: str, periods: int, df):
    """Predict future ratings using Linear Regression"""
    trend_result = analyze_rating_trend(professor_name, df)

    if "error" in trend_result:
        return trend_result

    dates = trend_result["dates"]
    ratings = trend_result["ratings"]

    X = np.arange(len(dates)).reshape(-1, 1)
    y = np.array(ratings)

    model = LinearRegression()
    model.fit(X, y)

    last_x = len(dates) - 1
    future_x = np.arange(last_x + 1, last_x + 1 + periods).reshape(-1, 1)
    future_predictions = model.predict(future_x)

    # คำนวณกรอบความน่าจะเป็น (Confidence Interval)
    residuals = y - model.predict(X)
    std_error = np.sqrt(np.sum(residuals**2) / (len(y) - 2)) if len(y) > 2 else 0.5
    margin = 1.96 * std_error

    lower_bound = future_predictions - margin
    upper_bound = future_predictions + margin

    # บีบให้อยู่ในกรอบคะแนน 1-5 ดาว
    future_predictions = np.clip(future_predictions, 1.0, 5.0)
    lower_bound = np.clip(lower_bound, 1.0, 5.0)
    upper_bound = np.clip(upper_bound, 1.0, 5.0)

    # สร้างวันที่อนาคต
    last_date_str = dates[-1]
    last_date = pd.to_datetime(last_date_str)

    future_dates = []
    for i in range(1, periods + 1):
        next_date = last_date + pd.DateOffset(months=i)
        future_dates.append(next_date.strftime('%Y-%m'))

    return {
        "professor": professor_name,
        "periods_predicted": periods,
        "historical": {
            "dates": dates,
            "ratings": ratings,
            "trend_line": trend_result["trend_line"]
        },
        "future": {
            "dates": future_dates,
            "predicted_ratings": np.round(future_predictions, 2).tolist(),
            "lower_bound": np.round(lower_bound, 2).tolist(),
            "upper_bound": np.round(upper_bound, 2).tolist()
        },
        "model_quality": trend_result["model_quality"],
        "trend_direction": trend_result["trend_direction"],
        "trend_percentage": trend_result["trend_percentage"]
    }


def compare_professors(professor_names: List[str], df):
    """Compare multiple professors"""
    results = {"total_professors": 0, "professors": [], "comparison": {}}
    found_professors = []

    for name in professor_names:
        pdf = df[df['professor_name'] == name]
        if len(pdf) == 0:
            continue

        avg_rating = round(pdf['quality'].mean(), 2)
        avg_difficulty = round(pdf['difficulty'].mean(), 2)
        num_ratings = len(pdf)
        rating_std = round(pdf['quality'].std(), 2) if num_ratings > 1 else 0.0

        # ใช้การสุ่มตรวจ Sentiment แค่ 50 คอมเมนต์ เพื่อให้ API ตอบกลับเร็วขึ้น
        sentiments = []
        from analytics import analyze_text
        for c in pdf['comments'].sample(min(50, len(pdf))):
            try:
                s, _ = analyze_text(c)
                sentiments.append(s)
            except Exception:
                pass # เผื่อกรณีไฟล์ analytics มีปัญหา จะได้ไม่พังทั้งระบบ

        sentiment_counts = pd.Series(sentiments).value_counts()
        total_sents = len(sentiments) if len(sentiments) > 0 else 1
        positive_pct = round((sentiment_counts.get('positive', 0) / total_sents) * 100, 1)
        negative_pct = round((sentiment_counts.get('negative', 0) / total_sents) * 100, 1)

        found_professors.append({
            "name": name,
            "avg_rating": avg_rating,
            "avg_difficulty": avg_difficulty,
            "num_ratings": num_ratings,
            "positive_percentage": positive_pct,
            "negative_percentage": negative_pct,
            "rating_std": rating_std
        })

    results["total_professors"] = len(found_professors)
    results["professors"] = found_professors

    if len(found_professors) > 0:
        results["comparison"] = {
            "highest_rated": max(found_professors, key=lambda x: x['avg_rating'])['name'],
            "lowest_rated": min(found_professors, key=lambda x: x['avg_rating'])['name'],
            "hardest": max(found_professors, key=lambda x: x['avg_difficulty'])['name'],
            "easiest": min(found_professors, key=lambda x: x['avg_difficulty'])['name'],
            "most_consistent": min(found_professors, key=lambda x: x['rating_std'])['name']
        }

    return results


def get_top_professors(by: str = "rating", n: int = 10, min_ratings: int = 5, df=None):
    """Get top N professors by various criteria"""
    if df is None:
        return {"error": "Dataset not provided"}

    prof_stats = df.groupby('professor_name').agg({
        'quality': ['mean', 'count', 'std'],
        'difficulty': 'mean'
    }).reset_index()

    prof_stats.columns = ['name', 'avg_rating', 'num_ratings', 'rating_std', 'avg_difficulty']
    prof_stats['rating_std'] = prof_stats['rating_std'].fillna(0.0) # จัดการค่า NaN กรณีรีวิวเดียว

    # กรองเอาเฉพาะคนที่มีรีวิวถึงเกณฑ์
    prof_stats = prof_stats[prof_stats['num_ratings'] >= min_ratings]

    # เรียงลำดับตามเงื่อนไข
    sort_logic = {
        "rating": ('avg_rating', False),
        "difficulty": ('avg_difficulty', False),
        "easiest": ('avg_difficulty', True),
        "hardest": ('avg_difficulty', False),
        "most_reviews": ('num_ratings', False),
        "most_consistent": ('rating_std', True)
    }
    
    col, asc = sort_logic.get(by, ('avg_rating', False))
    top_profs = prof_stats.sort_values(col, ascending=asc).head(n)

    result = []
    for _, row in top_profs.iterrows():
        result.append({
            "name": row['name'],
            "avg_rating": round(row['avg_rating'], 2),
            "avg_difficulty": round(row['avg_difficulty'], 2),
            "num_ratings": int(row['num_ratings']),
            "rating_std": round(row['rating_std'], 2)
        })

    return result

def get_predicted_rankings(n: int = 10, min_ratings: int = 5, df=None):
    if df is None: return []

    # 1. กรองเฉพาะอาจารย์ที่มีรีวิวถึงเกณฑ์
    prof_names = df['professor_name'].value_counts()
    valid_profs = prof_names[prof_names >= min_ratings].index.tolist()

    results = []
    for name in valid_profs:

        res = predict_future_rating(name, 1, df)
        
        if "error" not in res:
            results.append({
                "name": name,
                "avg_rating": round(df[df['professor_name'] == name]['quality'].mean(), 2),
                "predicted_rating": res["future"]["predicted_ratings"][0],
                "trend_direction": res["trend_direction"]
            })

    # 2. จัดอันดับตามคะแนนพยากรณ์จากมากไปน้อย
    sorted_results = sorted(results, key=lambda x: x['predicted_rating'], reverse=True)
    return sorted_results[:n]