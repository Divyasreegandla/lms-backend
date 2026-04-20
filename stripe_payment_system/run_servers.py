import subprocess
import sys
import os
import threading
import time

def run_fastapi():
    os.chdir("backend/fastapi_app")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def run_django():
    os.chdir("django_admin")
    subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8002"])

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Stripe Payment Integration for LMS")
    print("=" * 60)
    print("\n📌 Server URLs:")
    print("   FastAPI: http://localhost:8000")
    print("   Django Admin: http://localhost:8002/admin")
    print("\n💳 Test Cards:")
    print("   ✅ 4242 4242 4242 4242 (Success)")
    print("   🔐 4000 0025 0000 3155 (3D Secure)")
    print("\n📚 Checkout URLs:")
    print("   Course: http://localhost:8000/checkout/course/1")
    print("   Plan: http://localhost:8000/checkout/plan/1")
    print("\n⚠️  Press Ctrl+C to stop\n")
    print("=" * 60)
    
    threading.Thread(target=run_fastapi, daemon=True).start()
    time.sleep(2)
    threading.Thread(target=run_django, daemon=True).start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        sys.exit(0)