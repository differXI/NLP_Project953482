"""
Complete NLP Model Training Pipeline

Trains both sentiment and category classification models in one go.
Run this script to train all models from scratch.
"""

import subprocess
import sys
import os
from datetime import datetime


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: {description} failed!")
        print(f"Return code: {e.returncode}")
        return False


def main():
    """Run complete training pipeline"""
    print("\n" + "="*60)
    print(" " * 15 + "NLP MODEL TRAINING PIPELINE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check if data file exists
    data_path = "data/RateMyProfessor_Sample.csv"
    if not os.path.exists(data_path):
        print(f"\nERROR: Data file not found: {data_path}")
        print("Please ensure the data file is in the correct location.")
        sys.exit(1)

    print(f"\nData file: {data_path}")

    # Get file size
    file_size = os.path.getsize(data_path) / (1024 * 1024)  # Convert to MB
    print(f"File size: {file_size:.2f} MB")

    # Ask for confirmation if training from scratch
    print("\n" + "="*60)
    print("WARNING: This will overwrite existing models!")
    print("="*60)
    response = input("\nDo you want to continue? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        print("\nTraining cancelled.")
        return

    # Step 1: Train Sentiment Model
    print("\n" + "="*60)
    print("STEP 1: Train Sentiment Classification Model")
    print("="*60)

    success = run_command(
        f"{sys.executable} train_sentiment.py {data_path}",
        "Training Sentiment Model..."
    )

    if not success:
        print("\nFATAL: Sentiment model training failed!")
        print("Cannot continue with category training.")
        sys.exit(1)

    # Step 2: Train Category Model
    print("\n" + "="*60)
    print("STEP 2: Train Category Classification Model")
    print("="*60)

    success = run_command(
        f"{sys.executable} train_categories.py {data_path}",
        "Training Category Model..."
    )

    if not success:
        print("\nFATAL: Category model training failed!")
        sys.exit(1)

    # Success!
    print("\n" + "="*60)
    print(" " * 20 + "TRAINING COMPLETE!")
    print("="*60)

    print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n" + "="*60)
    print ("TRAINED MODELS")
    print("="*60)

    model_files = [
        ("models/vectorizer.pkl", "TF-IDF Vectorizer"),
        ("models/sentiment_model.pkl", "Sentiment Classifier"),
        ("models/category_model.pkl", "Category Classifier"),
        ("models/mlb.pkl", "MultiLabelBinarizer")
    ]

    all_exist = True
    for filepath, description in model_files:
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        print(f"{status} {description:40} ({filepath})")
        if not exists:
            all_exist = False

    if all_exist:
        print("\n" + "="*60)
        print("SUCCESS: All models trained and saved!")
        print("="*60)
        print("\nYou can now:")
        print("  1. Run the backend: python main.py")
        print("  2. Test models: python evaluate_models.py")
        print("  3. Start the frontend: cd ../frontend && npm start")
    else:
        print("\n" + "="*60)
        print("WARNING: Some model files are missing!")
        print("="*60)

    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
