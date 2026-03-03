import subprocess
import datetime
import sys
import os

def run_training():
    """Run complete training pipeline"""

    print("=" * 70)
    print(" " * 15 + "NLP MODEL TRAINING PIPELINE")
    print("=" * 70)
    print(f"Started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Ensure we're in the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    print(f"Working directory: {os.getcwd()}")
    print(f"Data path: data/RateMyProfessor_Sample.csv")
    print(f"Models path: models/\n")

    # Check if data file exists
    if not os.path.exists('data/RateMyProfessor_Sample.csv'):
        print("ERROR: data/RateMyProfessor_Sample.csv not found!")
        print("Please ensure the data file is in the data/ directory.")
        sys.exit(1)

    # Train sentiment model
    print("\n" + "=" * 70)
    print("[1/2] Training Sentiment Model...")
    print("=" * 70)
    result1 = subprocess.run([sys.executable, "train_sentiment.py"],
                           capture_output=False, text=True)

    if result1.returncode != 0:
        print("\n" + "!" * 70)
        print("ERROR: Sentiment training failed!")
        print("!" * 70)
        sys.exit(1)

    print("\n" + "✓" * 70)
    print("Sentiment model training completed successfully!")
    print("✓" * 70)

    # Train category model
    print("\n" + "=" * 70)
    print("[2/2] Training Category Model...")
    print("=" * 70)
    result2 = subprocess.run([sys.executable, "train_categories.py"],
                           capture_output=False, text=True)

    if result2.returncode != 0:
        print("\n" + "!" * 70)
        print("ERROR: Category training failed!")
        print("!" * 70)
        sys.exit(1)

    print("\n" + "✓" * 70)
    print("Category model training completed successfully!")
    print("✓" * 70)

    print("\n" + "=" * 70)
    print(" " * 20 + "ALL TRAINING COMPLETE!")
    print("=" * 70)
    print(f"Finished at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nModels saved:")
    print("  • models/vectorizer.pkl")
    print("  • models/sentiment_model.pkl")
    print("  • models/category_model.pkl")
    print("  • models/mlb.pkl")
    print("\nYou can now:")
    print("  • Run evaluate_models.py to test the models")
    print("  • Start the FastAPI server with: python main.py")
    print("=" * 70)

if __name__ == "__main__":
    try:
        run_training()
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        sys.exit(1)
