"""
views.py – Request handlers for the prompt generator app.

Views:
    index        – home page with input form + result display
    history      – paginated list of past inputs and prompts
    submit_feedback – AJAX-friendly feedback submission
    api_classify – JSON endpoint for client-side calls
"""

import json
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator
from django.utils import timezone

from .forms import PromptInputForm, FeedbackForm
from .models import UserInput, GeneratedPrompt, Feedback
from .ml.predictor import classify

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Home / index
# ---------------------------------------------------------------------------

def index(request):
    """
    GET  – Render empty form.
    POST – Validate form, run ML classification, save to DB, render result.
    """
    form   = PromptInputForm()
    result = None
    error  = None

    if request.method == 'POST':
        form = PromptInputForm(request.POST)

        if form.is_valid():
            raw_text = form.cleaned_data['input_text']
            selected_category = form.cleaned_data.get('selected_category') or None

            try:
                # ── ML classification ────────────────────────────────────
                prediction = classify(raw_text, selected_category=selected_category)

                # ── Persist to database ──────────────────────────────────
                user_input = UserInput.objects.create(
                    input_text=raw_text,
                    category=prediction.category,
                )
                generated = GeneratedPrompt.objects.create(
                    input_reference=user_input,
                    prompt_text=prediction.generated_prompt,
                    tone=prediction.tone,
                    confidence_score=prediction.confidence,
                )

                # ── Build result context ─────────────────────────────────
                result = {
                    'prompt':          prediction.generated_prompt,
                    'category':        prediction.category,
                    'tone':            prediction.tone,
                    'confidence':      prediction.confidence_pct,
                    'confidence_raw':  prediction.confidence,
                    'all_proba':       prediction.all_probabilities,
                    'input_id':        user_input.pk,
                    'prompt_id':       generated.pk,
                    'feedback_form':   FeedbackForm(),
                }

            except Exception as exc:
                logger.exception("ML classification failed: %s", exc)
                error = "Something went wrong during classification. Please try again."

        # Keep the form populated with the user's text on error
    return render(request, 'generator/index.html', {
        'form':   form,
        'result': result,
        'error':  error,
    })


# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------

def history(request):
    """
    Display a paginated history of all submitted inputs and their prompts.
    """
    inputs_qs  = UserInput.objects.select_related('generated_prompt').all()
    paginator  = Paginator(inputs_qs, 10)   # 10 items per page
    page_num   = request.GET.get('page', 1)
    page_obj   = paginator.get_page(page_num)

    return render(request, 'generator/history.html', {
        'page_obj': page_obj,
    })


# ---------------------------------------------------------------------------
# Feedback submission (AJAX-friendly)
# ---------------------------------------------------------------------------

@require_POST
def submit_feedback(request, prompt_id: int):
    """
    Accept feedback for a GeneratedPrompt.
    Works for both standard form POST and fetch() JSON.
    Returns JSON.
    """
    generated = get_object_or_404(GeneratedPrompt, pk=prompt_id)

    # Prevent duplicate feedback
    if hasattr(generated, 'feedback'):
        return JsonResponse({'status': 'already_submitted', 'message': 'Feedback already recorded.'})

    form = FeedbackForm(request.POST)
    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.generated_prompt = generated
        feedback.save()
        return JsonResponse({'status': 'ok', 'message': 'Thank you for your feedback!'})

    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


# ---------------------------------------------------------------------------
# JSON API endpoint (for optional fetch()-based UI)
# ---------------------------------------------------------------------------

@require_POST
def api_classify(request):
    """
    POST /api/classify/
    Body: { "text": "..." }
    Returns classification + generated prompt as JSON.
    """
    try:
        body = json.loads(request.body)
        text = body.get('text', '').strip()
        selected_category = body.get('selected_category') or None
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid JSON body.'}, status=400)

    if not text:
        return JsonResponse({'error': 'text field is required.'}, status=400)

    try:
        prediction = classify(text, selected_category=selected_category)
    except Exception as exc:
        logger.exception("API classify error: %s", exc)
        return JsonResponse({'error': str(exc)}, status=500)

    return JsonResponse({
        'category':         prediction.category,
        'confidence':       prediction.confidence_pct,
        'tone':             prediction.tone,
        'generated_prompt': prediction.generated_prompt,
        'all_probabilities': prediction.all_probabilities,
    })
