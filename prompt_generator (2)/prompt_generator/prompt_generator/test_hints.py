import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','prompt_generator.settings')
import django
django.setup()
from generator.ml.predictor import classify

tests = [
    'Write a short story about a robot discovering emotions',
    'Explain how neural networks work to a complete beginner',
    'Help me write a pitch deck for my SaaS startup',
    'Fix my Python async function that keeps raising a RuntimeError',
    'Analyze the pros and cons of remote work culture'
]

print("Testing all hint pills:\n")
for text in tests:
    result = classify(text)
    print(f"{text[:50]:50} -> {result.category}")
