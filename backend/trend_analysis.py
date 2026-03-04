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
from sklearn.preprocessing import PolynomialFeatures
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def add_synthetic_dates(df):
    """
    Add synthetic date column if not present

    Args:
        df: DataFrame with professor data

    Returns:
        DataFrame with post_date column added
    """
    if 'post_date' in df.columns:
        return df

    # Create synthetic dates spread over 2 years
    np.random.seed(42)
    n_samples = len(df)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 1, 1)

    random_dates = pd.to_datetime(np.random.uniform(
        start_date.timestamp(),
        end_date.timestamp(),
        n_samples
    ), unit='s')

    df = df.copy()
    df['post_date'] = random_dates

    return df


def analyze_rating_trend(professor_name: str, df):
    """
    Analyze rating trend for a specific professor

    Args:
        professor_name: Name of the professor
        df: Full dataset DataFrame

    Returns:
        Dictionary containing trend analysis results
    """
    # Check if professor exists
    pdf = df[df['professor_name'] == professor_name]

    if len(pdf) == 0:
        return {
            "error": f"Professor '{professor_name}' not found",
            "available_professors": df['professor_name'].unique().tolist()[:10]
        }

    # Ensure we have date column
    pdf = add_synthetic_dates(pdf)

    # Group by month for trend analysis
    pdf['year_month'] = pd.to_datetime(pdf['post_date']).dt.to_period('M')

    # Calculate monthly averages
    monthly_data = pdf.groupby('year_month').agg({
        'quality': ['mean', 'count']
    }).reset_index()

    monthly_data.columns = ['year_month', 'avg_rating', 'num_ratings']

    # Filter to ensure we have enough data points
    if len(monthly_data) < 3:
        return {
            "error": f"Not enough data points for '{professor_name}'. Only {len(monthly_data)} months of data.",
            "min_months_required": 3
        }

    # Sort by date
    monthly_data = monthly_data.sort_values('year_month')
    monthly_data['year_month'] = monthly_data['year_month'].astype(str)

    # Prepare data for regression
    X = np.arange(len(monthly_data)).reshape(-1, 1)
    y = monthly_data['avg_rating'].values

    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)

    # Calculate trend line
    trend_line = model.predict(X)

    # Calculate R-squared
    y_mean = np.mean(y)
    ss_tot = np.sum((y - y_mean) ** 2)
    ss_res = np.sum((y - trend_line) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    # Determine trend direction
    slope = model.coef_[0]
    if slope > 0.01:
        trend_direction = "increasing"
    elif slope < -0.01:
        trend_direction = "decreasing"
    else:
        trend_direction = "stable"

    # Calculate percentage change
    if len(y) >= 2:
        first_avg = y[0]
        last_avg = y[-1]
        trend_percentage = ((last_avg - first_avg) / first_avg) * 100
    else:
        trend_percentage = 0

    return {
        "professor": professor_name,
        "dates": monthly_data['year_month'].tolist(),
        "ratings": monthly_data['avg_rating'].tolist(),
        "num_ratings_per_month": monthly_data['num_ratings'].tolist(),
        "trend_line": trend_line.tolist(),
        "trend_direction": trend_direction,
        "trend_percentage": round(trend_percentage, 2),
        "model_quality": {
            "r_squared": round(r_squared, 3),
            "slope": round(slope, 4)
        },
        "data_points": len(monthly_data)
    }


def predict_future_rating(professor_name: str, periods: int, df):
    """
    Predict future ratings using Linear Regression

    Args:
        professor_name: Name of the professor
        periods: Number of future periods to predict
        df: Full dataset DataFrame

    Returns:
        Dictionary containing prediction results
    """
    # Get historical trend data first
    trend_result = analyze_rating_trend(professor_name, df)

    if "error" in trend_result:
        return trend_result

    # Prepare historical data
    dates = trend_result["dates"]
    ratings = trend_result["ratings"]

    # Create numerical X values
    X = np.arange(len(dates)).reshape(-1, 1)
    y = np.array(ratings)

    # Fit model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future periods
    last_x = len(dates) - 1
    future_x = np.arange(last_x + 1, last_x + 1 + periods).reshape(-1, 1)
    future_predictions = model.predict(future_x)

    # Calculate confidence intervals (using residual standard error)
    residuals = y - model.predict(X)
    std_error = np.sqrt(np.sum(residuals**2) / (len(y) - 2))
    margin = 1.96 * std_error  # 95% confidence interval

    lower_bound = future_predictions - margin
    upper_bound = future_predictions + margin

    # Clip to valid rating range [1, 5]
    future_predictions = np.clip(future_predictions, 1, 5)
    lower_bound = np.clip(lower_bound, 1, 5)
    upper_bound = np.clip(upper_bound, 1, 5)

    # Generate future dates (monthly)
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
    """
    Compare multiple professors

    Args:
        professor_names: List of professor names to compare
        df: Full dataset DataFrame

    Returns:
        Dictionary containing comparison results
    """
    results = {
        "total_professors": 0,
        "professors": [],
        "comparison": {}
    }

    found_professors = []

    for name in professor_names:
        pdf = df[df['professor_name'] == name]

        if len(pdf) == 0:
            continue

        # Calculate statistics
        avg_rating = round(pdf['quality'].mean(), 2)
        avg_difficulty = round(pdf['difficulty'].mean(), 2)
        num_ratings = len(pdf)

        # Calculate sentiment percentages
        sentiments = []
        for c in pdf['comments'].sample(min(50, len(pdf))):
            from analytics import analyze_text
            s, _ = analyze_text(c)
            sentiments.append(s)

        sentiment_counts = pd.Series(sentiments).value_counts()
        positive_pct = round((sentiment_counts.get('positive', 0) / len(sentiments)) * 100, 1)
        negative_pct = round((sentiment_counts.get('negative', 0) / len(sentiments)) * 100, 1)

        # Rating std (consistency measure)
        rating_std = round(pdf['quality'].std(), 2)

        prof_data = {
            "name": name,
            "avg_rating": avg_rating,
            "avg_difficulty": avg_difficulty,
            "num_ratings": num_ratings,
            "positive_percentage": positive_pct,
            "negative_percentage": negative_pct,
            "rating_std": rating_std
        }

        found_professors.append(prof_data)

    results["total_professors"] = len(found_professors)
    results["professors"] = found_professors

    # Add comparison rankings
    if len(found_professors) > 0:
        # Sort by different criteria
        sorted_by_rating = sorted(found_professors, key=lambda x: x['avg_rating'], reverse=True)
        sorted_by_difficulty = sorted(found_professors, key=lambda x: x['avg_difficulty'], reverse=True)
        sorted_by_easiest = sorted(found_professors, key=lambda x: x['avg_difficulty'])
        sorted_by_consistent = sorted(found_professors, key=lambda x: x['rating_std'])

        results["comparison"] = {
            "highest_rated": sorted_by_rating[0]['name'],
            "lowest_rated": sorted_by_rating[-1]['name'],
            "hardest": sorted_by_difficulty[0]['name'],
            "easiest": sorted_by_easiest[0]['name'],
            "most_consistent": sorted_by_consistent[0]['name']
        }

    return results


def get_top_professors(by: str = "rating", n: int = 10, min_ratings: int = 5, df=None):
    """
    Get top N professors by various criteria

    Args:
        by: Sorting criteria
        n: Number of professors to return
        min_ratings: Minimum number of ratings required
        df: Dataset DataFrame

    Returns:
        List of top professors
    """
    if df is None:
        return {"error": "Dataset not provided"}

    # Group by professor and calculate statistics
    prof_stats = df.groupby('professor_name').agg({
        'quality': ['mean', 'count', 'std'],
        'difficulty': 'mean'
    }).reset_index()

    prof_stats.columns = ['name', 'avg_rating', 'num_ratings', 'rating_std', 'avg_difficulty']

    # Filter by minimum ratings
    prof_stats = prof_stats[prof_stats['num_ratings'] >= min_ratings]

    # Sort by criteria
    if by == "rating":
        sorted_profs = prof_stats.sort_values('avg_rating', ascending=False)
    elif by == "difficulty":
        sorted_profs = prof_stats.sort_values('avg_difficulty', ascending=False)
    elif by == "easiest":
        sorted_profs = prof_stats.sort_values('avg_difficulty', ascending=True)
    elif by == "hardest":
        sorted_profs = prof_stats.sort_values('avg_difficulty', ascending=False)
    elif by == "most_reviews":
        sorted_profs = prof_stats.sort_values('num_ratings', ascending=False)
    elif by == "most_consistent":
        sorted_profs = prof_stats.sort_values('rating_std', ascending=True)
    else:
        sorted_profs = prof_stats.sort_values('avg_rating', ascending=False)

    # Take top N
    top_profs = sorted_profs.head(n)

    # Convert to list of dictionaries
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
