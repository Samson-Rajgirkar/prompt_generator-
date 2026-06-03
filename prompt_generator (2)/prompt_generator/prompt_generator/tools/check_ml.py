import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','prompt_generator.settings')
import django
django.setup()
from generator.ml.predictor import classify
from generator.models import UserInput, GeneratedPrompt

print('Running ML + DB test...')
res = classify('write a short story about a dragon')
print('CATEGORY:', res.category)
print('TONE:', res.tone)
print('CONF:', res.confidence_pct)

ui = UserInput.objects.create(input_text='test insert from check script', category=res.category)
gp = GeneratedPrompt.objects.create(input_reference=ui, prompt_text=res.generated_prompt, tone=res.tone, confidence_score=res.confidence)
print('Inserted prompt id:', gp.pk)
