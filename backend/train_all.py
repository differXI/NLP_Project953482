"""
Complete NLP Model Training Pipeline
Run this script to train all models from scratch automatically.
"""

import subprocess
import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ==========================================
# ⚙️ SETTINGS
# ==========================================
CONFIG = {
    "data_path": os.path.join(BASE_DIR, "data", "RateMyProfessor_Sample.csv"),
    "models_dir": os.path.join(BASE_DIR, "models"),
    "python_exe": sys.executable # ใช้ Python เวอร์ชั่นปัจจุบันที่กำลังรันสคริปต์นี้
}

def run_script(script_name, description):
    """รันไฟล์ Python ย่อย พร้อมจัดการ Error ให้สวยงาม"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    # 🌟 สร้าง Path เต็มๆ ให้สคริปต์ที่จะรันด้วย
    script_path = os.path.join(BASE_DIR, script_name)

    # ประกอบร่างคำสั่ง (ใช้ Path เต็มๆ ทุกจุด)
    command = f'"{CONFIG["python_exe"]}" "{script_path}" "{CONFIG["data_path"]}"'
    try:
        # ใช้ subprocess.run เพื่อแสดงผลลัพธ์ (Logs) จากไฟล์ย่อยขึ้นจอแบบสดๆ
        subprocess.run(
            command,
            shell=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR: {script_name} failed to execute!")
        return False

def main():
    print("\n" + "="*60)
    print("🎓 NLP MODEL TRAINING PIPELINE 🎓".center(60))
    print("="*60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. เช็คไฟล์ข้อมูล
    if not os.path.exists(CONFIG["data_path"]):
        print(f"\n❌ FATAL ERROR: Data file not found -> '{CONFIG['data_path']}'")
        print("Please check the 'data_path' in CONFIG.")
        sys.exit(1)
    
    file_size_mb = os.path.getsize(CONFIG["data_path"]) / (1024 * 1024)
    print(f"Dataset: {CONFIG['data_path']} ({file_size_mb:.2f} MB)")

    # 2. ยืนยันก่อนเริ่มเทรน (ป้องกันมือลั่นไปกดรันแล้วเซฟทับของเก่า)
    print("\n⚠️ WARNING: This will overwrite your existing models in the 'models/' folder.")
    response = input("Do you want to proceed? (yes/y to continue): ").strip().lower()

    if response not in ['yes', 'y']:
        print("\n🛑 Training cancelled by user.")
        return

    # 3. รันเทรนโมเดลตามลำดับ (Sentiment ต้องมาก่อนเสมอ!)
    if not run_script("train_sentiment.py", "STEP 1: Train Sentiment Classification Model"):
        print("\n❌ PIPELINE HALTED: Sentiment training failed. Cannot proceed to Category model.")
        sys.exit(1)

    if not run_script("train_categories.py", "STEP 2: Train Category Classification Model"):
        print("\n❌ PIPELINE HALTED: Category training failed.")
        sys.exit(1)

    # 4. สรุปผล
    print("\n" + "="*60)
    print("✨ ALL TRAINING COMPLETED SUCCESSFULLY ✨".center(60))
    print("="*60)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ตรวจสอบว่าไฟล์ถูกสร้างขึ้นมาครบจริงๆ ไหม
    expected_files = [
        "vectorizer.pkl",
        "sentiment_model.pkl",
        "category_model.pkl",
        "mlb.pkl"
    ]

    missing = False
    print("\nVerifying output files in 'models/' directory:")
    for file_name in expected_files:
        filepath = os.path.join(CONFIG["models_dir"], file_name)
        if os.path.exists(filepath):
            print(f"  ✅ Found: {file_name}")
        else:
            print(f"  ❌ MISSING: {file_name}")
            missing = True

    if missing:
        print("\n⚠️ WARNING: Some model files are missing. Check the logs above for errors.")
    else:
        print("\n🎉 You are ready to run the API: uvicorn main:app --reload --port 8000")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Training manually interrupted (Ctrl+C).")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}")
        sys.exit(1)