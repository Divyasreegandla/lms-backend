import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "django_app"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.lms.settings")

django.setup()