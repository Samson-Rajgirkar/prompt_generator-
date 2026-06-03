import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','prompt_generator.settings')
import django
django.setup()
from generator.ml.predictor import classify

user_text = "My age is 21, height is 5'8 inch and the body weight is 55kg i want to gain 5kg of weight within a week so create a so create a well defined routine for me"

result = classify(user_text)
print(f"User text: {user_text[:60]}...")
print(f"Classified as: {result.category}")
print(f"Confidence: {result.confidence_pct}")
print(f"\nTone: {result.tone}")
