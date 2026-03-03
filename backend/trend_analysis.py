import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import os

def load_data():
    """Load the dataset"""
    DATA_PATH = "data/RateMyProfessor_Sample.csv"
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found!")

    df = pd.read_csv(DATA_PATH)
    df = df[['professor_name', 'star_rating', 'student_difficult', 'comments']].dropna()
    df = df.rename(columns={
        "star_rating": "quality",
        "student_difficult": "difficulty"
    })

    # Add a synthetic date column if not present (for demonstration)
    # In real scenario, you would have actual post_date
    if 'post_date' not in df.columns:
        # Create synthetic dates based on index (simulate time series)
        # Spread ratings over 2 years period
        n_samples = len(df)
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2024, 1, 1)

        # Assign random dates weighted to be more recent
        random_dates = pd.to_datetime(np.random.uniform(
            start_date.timestamp(),
            end_date.timestamp(),
            n_samples
        ), unit='s')

        df['post_date'] = random_dates

    return df

def analyze_rating_trend(professor_name: str, df: pd.DataFrame = None) -> Dict:
    """
    Analyze trend ของ rating ตามเวลา

    Args:
        professor_name: ชื่ออาจารย์
        df: DataFrame (optional, will load if not provided)

    Returns:
        Dictionary ที่มี:
        - dates: list of dates
        - ratings: list of actual ratings
        - trend_line: list of trend values
        - r_squared: R² score
        - slope: trend slope (positive = increasing, negative = decreasing)
        - trend_direction: 'increasing', 'decreasing', or 'stable'
    """
    if df is None:
        df = load_data()

    # Filter for specific professor
    pdf = df[df["professor_name"] == professor_name].copy()

    if len(pdf) < 3:
        return {
            "error": f"Not enough data for {professor_name} (need at least 3 ratings)"
        }

    # Sort by date
    pdf = pdf.sort_values('post_date')

    # Convert dates to numeric (days since first date)
    pdf['days_since_start'] = (pdf['post_date'] - pdf['post_date'].iloc[0]).dt.days

    # Get ratings
    ratings = pdf['quality'].values
    days = pdf['days_since_start'].values.reshape(-1, 1)

    # Fit linear regression
    model = LinearRegression()
    model.fit(days, ratings)

    # Calculate trend line
    trend_line = model.predict(days)

    # Calculate R²
    ss_res = ((ratings - trend_line) ** 2).sum()
    ss_tot = ((ratings - ratings.mean()) ** 2).sum()
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    # Determine trend direction
    slope = model.coef_[0]
    slope_scaled = slope * 30  # Scale to monthly change

    if slope_scaled > 0.05:
        trend_direction = "increasing"
        trend_percentage = f"+{slope_scaled * 100:.1f}%"
    elif slope_scaled < -0.05:
        trend_direction = "decreasing"
        trend_percentage = f"{slope_scaled * 100:.1f}%"
    else:
        trend_direction = "stable"
        trend_percentage = "±0.0%"

    return {
        "professor": professor_name,
        "dates": pdf['post_date'].dt.strftime('%Y-%m-%d').tolist(),
        "ratings": ratings.tolist(),
        "trend_line": trend_line.tolist(),
        "r_squared": round(r_squared, 3),
        "slope": round(slope, 4),
        "slope_monthly": round(slope_scaled, 4),
        "trend_direction": trend_direction,
        "trend_percentage": trend_percentage,
        "data_points": len(pdf)
    }

def predict_future_rating(professor_name: str, periods: int = 5,
                          df: pd.DataFrame = None) -> Dict:
    """
    ทำนาย rating ในอนาคตด้วย Linear Regression

    Args:
        professor_name: ชื่ออาจารย์
        periods: จำนวนคาบเวลาที่ต้องการทำนาย (default: 5 future data points)
        df: DataFrame (optional)

    Returns:
        Dictionary ที่มี:
        - historical_dates: past dates
        - historical_ratings: past actual ratings
        - historical_trend: past trend line
        - future_dates: predicted future dates
        - predicted_ratings: predicted future ratings
        - confidence_interval: lower/upper bounds
    """
    if df is None:
        df = load_data()

    # Get trend analysis first
    trend_result = analyze_rating_trend(professor_name, df)

    if "error" in trend_result:
        return trend_result

    pdf = df[df["professor_name"] == professor_name].copy()
    pdf = pdf.sort_values('post_date')

    # Calculate average time gap between ratings
    pdf['days_since_start'] = (pdf['post_date'] - pdf['post_date'].iloc[0]).dt.days

    # Fit model on all data
    model = LinearRegression()
    X = pdf['days_since_start'].values.reshape(-1, 1)
    y = pdf['quality'].values
    model.fit(X, y)

    # Calculate prediction interval (simple version using std of residuals)
    predictions = model.predict(X)
    residuals = y - predictions
    std_error = np.std(residuals)
    confidence_margin = 1.96 * std_error  # 95% confidence

    # Generate future dates
    last_date = pdf['post_date'].iloc[-1]
    avg_gap_days = (pdf['post_date'].iloc[-1] - pdf['post_date'].iloc[0]).days / (len(pdf) - 1)

    future_dates = []
    future_days = []

    for i in range(1, periods + 1):
        next_date = last_date + timedelta(days=avg_gap_days * i)
        future_dates.append(next_date.strftime('%Y-%m-%d'))
        future_days.append((next_date - pdf['post_date'].iloc[0]).days)

    # Predict future ratings
    future_X = np.array(future_days).reshape(-1, 1)
    predicted_ratings = model.predict(future_X)

    # Calculate confidence intervals
    lower_bound = predicted_ratings - confidence_margin
    upper_bound = predicted_ratings + confidence_margin
    lower_bound = np.clip(lower_bound, 1, 5)
    upper_bound = np.clip(upper_bound, 1, 5)

    return {
        "professor": professor_name,
        "historical": {
            "dates": pdf['post_date'].dt.strftime('%Y-%m-%d').tolist(),
            "ratings": y.tolist(),
            "trend_line": predictions.tolist()
        },
        "future": {
            "dates": future_dates,
            "predicted_ratings": predicted_ratings.tolist(),
            "lower_bound": lower_bound.tolist(),
            "upper_bound": upper_bound.tolist()
        },
        "next_semester_prediction": round(float(predicted_ratings[0]), 2),
        "confidence": 95,
        "model_quality": {
            "r_squared": trend_result["r_squared"],
            "trend_direction": trend_result["trend_direction"]
        }
    }

def compare_professors(professor_names: List[str], df: pd.DataFrame = None) -> Dict:
    """
    เปรียบเทียบข้อมูลหลายอาจารย์

    Args:
        professor_names: list of professor names
        df: DataFrame (optional)

    Returns:
        Dictionary with comparison data
    """
    if df is None:
        df = load_data()

    comparison_data = []

    for name in professor_names:
        pdf = df[df["professor_name"] == name]

        if len(pdf) == 0:
            continue

        avg_rating = round(pdf["quality"].mean(), 2)
        avg_difficulty = round(pdf["difficulty"].mean(), 2)
        num_ratings = len(pdf)
        rating_std = round(pdf["quality"].std(), 2)

        # Get sentiment distribution (simplified)
        positive_count = len(pdf[pdf["quality"] >= 4.0])
        negative_count = len(pdf[pdf["quality"] < 3.0])

        comparison_data.append({
            "name": name,
            "avg_rating": avg_rating,
            "avg_difficulty": avg_difficulty,
            "num_ratings": num_ratings,
            "rating_std": rating_std,
            "positive_percentage": round(positive_count / num_ratings * 100, 1),
            "negative_percentage": round(negative_count / num_ratings * 100, 1)
        })

    # Sort by average rating
    comparison_data.sort(key=lambda x: x["avg_rating"], reverse=True)

    return {
        "professors": comparison_data,
        "total_professors": len(comparison_data)
    }

def get_top_professors(by: str = "rating", n: int = 10,
                       min_ratings: int = 5, df: pd.DataFrame = None) -> Dict:
    """
    ดู top N อาจารย์ตาม criteria ที่เลือก

    Args:
        by: "rating", "difficulty", "easiest", "hardest", "most_reviews"
        n: number of top professors to return
        min_ratings: minimum number of ratings required
        df: DataFrame (optional)

    Returns:
        Dictionary with top professors
    """
    if df is None:
        df = load_data()

    # Group by professor
    prof_stats = df.groupby("professor_name").agg({
        "quality": ["mean", "std", "count"],
        "difficulty": ["mean", "std"]
    }).round(2)

    prof_stats.columns = ["avg_rating", "rating_std", "num_ratings",
                         "avg_difficulty", "difficulty_std"]

    # Filter by minimum ratings
    prof_stats = prof_stats[prof_stats["num_ratings"] >= min_ratings]

    if by == "rating":
        top_profs = prof_stats.nlargest(n, "avg_rating")
    elif by == "difficulty":
        top_profs = prof_stats.nlargest(n, "avg_difficulty")
    elif by == "easiest":
        top_profs = prof_stats.nsmallest(n, "avg_difficulty")
    elif by == "most_reviews":
        top_profs = prof_stats.nlargest(n, "num_ratings")
    elif by == "most_consistent":
        # Least rating standard deviation (with at least 5 ratings)
        prof_stats_filtered = prof_stats[prof_stats["num_ratings"] >= 5]
        top_profs = prof_stats_filtered.nsmallest(n, "rating_std")
    else:
        top_profs = prof_stats.nlargest(n, "avg_rating")

    return {
        "criteria": by,
        "top_professors": [
            {
                "name": idx,
                "avg_rating": row["avg_rating"],
                "avg_difficulty": row["avg_difficulty"],
                "num_ratings": int(row["num_ratings"])
            }
            for idx, row in top_profs.iterrows()
        ]
    }
