import pandas as pd
import numpy as np
from typing import Optional, Dict, List
import os

def load_rate_my_professor(path: str = "data/RateMyProfessor_Sample.csv") -> pd.DataFrame:
    """
    Load RateMyProfessor dataset

    Args:
        path: Path to the CSV file

    Returns:
        DataFrame with normalized columns
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"RateMyProfessor data not found at {path}")

    df = pd.read_csv(path)

    # Standardize column names
    column_mapping = {
        "professor_name": "professor_name",
        "department_name": "course",
        "star_rating": "quality",
        "student_difficult": "difficulty",
        "comments": "comments"
    }

    # Keep only relevant columns
    available_cols = [col for col in column_mapping.values() if col in df.columns]

    # Try alternative column names
    if 'star_rating' not in df.columns:
        # Map alternative column names
        alt_mapping = {
            'rating': 'quality',
            'overall_rating': 'quality',
            'stars': 'quality'
        }
        for alt, std in alt_mapping.items():
            if alt in df.columns:
                df = df.rename(columns={alt: std})
                break

    if 'student_difficult' not in df.columns:
        alt_mapping = {
            'difficulty': 'difficulty',
            'student_diff': 'difficulty',
            'level_of_difficulty': 'difficulty'
        }
        for alt, std in alt_mapping.items():
            if alt in df.columns:
                df = df.rename(columns={alt: std})
                break

    # Select relevant columns
    required_cols = ['professor_name', 'quality', 'comments']
    optional_cols = ['course', 'difficulty']

    cols_to_use = [col for col in required_cols if col in df.columns]
    cols_to_use += [col for col in optional_cols if col in df.columns]

    df = df[cols_to_use].dropna(subset=['professor_name', 'quality', 'comments'])

    # Rename to standard names
    rename_map = {}
    if 'course' not in df.columns and 'department_name' in df.columns:
        rename_map['department_name'] = 'course'
    df = df.rename(columns=rename_map)

    # Add dataset source
    df['data_source'] = 'RateMyProfessor'

    return df


def load_coursera(path: str = "data/Coursera_reviews.csv") -> pd.DataFrame:
    """
    Load Coursera course reviews dataset

    Note: This is a template function. Adjust column mappings based on actual
    Coursera dataset structure.

    Common Coursera dataset columns:
    - course_id / course_name
    - rating / score
    - reviews / comments
    - date (optional)

    Args:
        path: Path to the Coursera CSV file

    Returns:
        DataFrame with normalized columns matching RateMyProfessor format
    """
    if not os.path.exists(path):
        # Return empty DataFrame if file doesn't exist
        print(f"Warning: Coursera data not found at {path}")
        return pd.DataFrame()

    df = pd.read_csv(path)

    # Map Coursera columns to our standard format
    # Adjust these based on your actual Coursera dataset structure
    column_mapping = {
        # Common Coursera column names -> Standard names
        'course_name': 'course',
        'course': 'course',
        'course_id': 'course',
        'rating': 'quality',
        'score': 'quality',
        'star_rating': 'quality',
        'review': 'comments',
        'reviews': 'comments',
        'comment': 'comments',
        'text': 'comments'
    }

    # Rename columns based on mapping
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})

    # Ensure we have required columns
    if 'comments' not in df.columns:
        raise ValueError("Coursera dataset must have a comment/review column")

    if 'quality' not in df.columns:
        raise ValueError("Coursera dataset must have a rating/score column")

    # Create a synthetic professor name from course (since Coursera is course-based)
    if 'professor_name' not in df.columns:
        df['professor_name'] = df['course'] + ' (Instructor)'

    # Ensure difficulty column exists (set to neutral if not present)
    if 'difficulty' not in df.columns:
        df['difficulty'] = 3.0  # Neutral difficulty

    # Select and clean
    required_cols = ['professor_name', 'quality', 'comments']
    optional_cols = ['course', 'difficulty']

    cols_to_use = [col for col in required_cols if col in df.columns]
    cols_to_use += [col for col in optional_cols if col in df.columns]

    df = df[cols_to_use].dropna(subset=['professor_name', 'quality', 'comments'])

    # Add dataset source
    df['data_source'] = 'Coursera'

    return df


def normalize_datasets(rmp_df: pd.DataFrame, coursera_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Normalize and combine datasets

    Args:
        rmp_df: RateMyProfessor DataFrame
        coursera_df: Coursera DataFrame (optional)

    Returns:
        Combined DataFrame with standardized columns
    """
    # Ensure we have RateMyProfessor data
    if rmp_df.empty:
        raise ValueError("RateMyProfessor data cannot be empty")

    # Standardize column names for RMP
    rmp_df = rmp_df.copy()
    if 'data_source' not in rmp_df.columns:
        rmp_df['data_source'] = 'RateMyProfessor'

    datasets = [rmp_df]

    # Add Coursera if available
    if coursera_df is not None and not coursera_df.empty:
        coursera_df = coursera_df.copy()
        if 'data_source' not in coursera_df.columns:
            coursera_df['data_source'] = 'Coursera'
        datasets.append(coursera_df)

    # Combine
    combined_df = pd.concat(datasets, ignore_index=True)

    # Normalize rating scales (ensure 1-5)
    combined_df['quality'] = combined_df['quality'].clip(1, 5)

    # Normalize difficulty (ensure 1-5)
    if 'difficulty' in combined_df.columns:
        combined_df['difficulty'] = combined_df['difficulty'].clip(1, 5)
    else:
        combined_df['difficulty'] = 3.0  # Default neutral

    # Clean text
    combined_df['comments'] = combined_df['comments'].astype(str).str.strip()
    combined_df = combined_df[combined_df['comments'] != '']

    # Remove duplicates
    combined_df = combined_df.drop_duplicates(subset=['professor_name', 'comments'])

    return combined_df


def load_combined_dataset(
    rmp_path: str = "data/RateMyProfessor_Sample.csv",
    coursera_path: str = "data/Coursera_reviews.csv",
    save_combined: bool = True,
    output_path: str = "data/combined_dataset.csv"
) -> pd.DataFrame:
    """
    Load and combine both datasets

    Args:
        rmp_path: Path to RateMyProfessor data
        coursera_path: Path to Coursera data
        save_combined: Whether to save the combined dataset
        output_path: Path to save combined dataset

    Returns:
        Combined DataFrame
    """
    print("=" * 60)
    print("LOADING COMBINED DATASET")
    print("=" * 60)

    # Load RateMyProfessor
    print("\n[1/3] Loading RateMyProfessor data...")
    rmp_df = load_rate_my_professor(rmp_path)
    print(f"  ✓ Loaded {len(rmp_df)} reviews from RateMyProfessor")

    # Load Coursera (optional)
    print("\n[2/3] Loading Coursera data...")
    try:
        coursera_df = load_coursera(coursera_path)
        if not coursera_df.empty:
            print(f"  ✓ Loaded {len(coursera_df)} reviews from Coursera")
        else:
            print(f"  ⚠ Coursera data not available (using only RateMyProfessor)")
            coursera_df = None
    except Exception as e:
        print(f"  ⚠ Could not load Coursera data: {e}")
        print(f"  Using only RateMyProfessor data")
        coursera_df = None

    # Normalize and combine
    print("\n[3/3] Normalizing and combining datasets...")
    combined_df = normalize_datasets(rmp_df, coursera_df)

    # Add synthetic dates for trend analysis
    if 'post_date' not in combined_df.columns:
        print("  Adding synthetic dates for trend analysis...")
        np.random.seed(42)
        n_samples = len(combined_df)
        from datetime import datetime, timedelta

        # Create dates spread over 2 years
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2024, 1, 1)

        random_dates = pd.to_datetime(np.random.uniform(
            start_date.timestamp(),
            end_date.timestamp(),
            n_samples
        ), unit='s')

        combined_df['post_date'] = random_dates

    # Display statistics
    print(f"\n  ✓ Combined dataset: {len(combined_df)} total reviews")
    print(f"\n  Data source breakdown:")
    print(f"    RateMyProfessor: {len(combined_df[combined_df['data_source'] == 'RateMyProfessor'])}")
    if coursera_df is not None:
        print(f"    Coursera: {len(combined_df[combined_df['data_source'] == 'Coursera'])}")

    print(f"\n  Rating distribution:")
    print(combined_df['quality'].describe())

    print(f"\n  Unique professors: {combined_df['professor_name'].nunique()}")

    # Save combined dataset
    if save_combined:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        combined_df.to_csv(output_path, index=False)
        print(f"\n  ✓ Saved combined dataset to {output_path}")

    print("\n" + "=" * 60)
    print("DATASET LOADING COMPLETE")
    print("=" * 60)

    return combined_df


def get_dataset_statistics(df: pd.DataFrame) -> Dict:
    """
    Get statistics about the dataset

    Args:
        df: The dataset DataFrame

    Returns:
        Dictionary with statistics
    """
    stats = {
        "total_reviews": len(df),
        "unique_professors": df['professor_name'].nunique(),
        "unique_courses": df['course'].nunique() if 'course' in df.columns else 'N/A',
        "avg_rating": round(df['quality'].mean(), 2),
        "avg_difficulty": round(df['difficulty'].mean(), 2) if 'difficulty' in df.columns else 'N/A',
        "rating_std": round(df['quality'].std(), 2),
        "data_sources": df['data_source'].value_counts().to_dict() if 'data_source' in df.columns else {},
        "date_range": {
            "start": df['post_date'].min().strftime('%Y-%m-%d') if 'post_date' in df.columns else 'N/A',
            "end": df['post_date'].max().strftime('%Y-%m-%d') if 'post_date' in df.columns else 'N/A'
        }
    }

    return stats


if __name__ == "__main__":
    # Test the data loader
    try:
        df = load_combined_dataset()

        print("\n" + "=" * 60)
        print("DATASET STATISTICS")
        print("=" * 60)

        stats = get_dataset_statistics(df)

        for key, value in stats.items():
            if isinstance(value, dict):
                print(f"\n{key.upper()}:")
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
