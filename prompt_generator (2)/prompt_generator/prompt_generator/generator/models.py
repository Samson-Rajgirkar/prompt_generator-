"""
models.py – Database models for the prompt generator application.

Tables:
    UserInput       – stores raw user input with detected category
    GeneratedPrompt – stores the AI-generated prompt linked to a UserInput
    Feedback        – optional user rating/comment on a generated prompt
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# ---------------------------------------------------------------------------
# Choices
# ---------------------------------------------------------------------------
CATEGORY_CHOICES = [
    ('creative',       'Creative'),
    ('fitness',        'Gym / Fitness'),
    ('technical',      'Technical'),
    ('analytical',     'Analytical'),
    ('educational',    'Educational'),
    ('business',       'Business'),
    ('conversational', 'Conversational'),
]

TONE_CHOICES = [
    ('formal',     'Formal'),
    ('casual',     'Casual'),
    ('detailed',   'Detailed'),
    ('concise',    'Concise'),
    ('creative',   'Creative'),
    ('technical',  'Technical'),
    ('persuasive', 'Persuasive'),
    ('simple',     'Simple'),
]

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]   # 1–5 stars


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class UserInput(models.Model):
    """Represents a single user query submitted through the form."""

    input_text  = models.TextField(
        verbose_name="User Input",
        help_text="The raw text entered by the user.",
    )
    category    = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="Detected Category",
    )
    timestamp   = models.DateTimeField(auto_now_add=True, verbose_name="Submitted At")

    class Meta:
        ordering         = ['-timestamp']
        verbose_name     = 'User Input'
        verbose_name_plural = 'User Inputs'

    def __str__(self):
        snippet = self.input_text[:60] + ('…' if len(self.input_text) > 60 else '')
        return f"[{self.category}] {snippet}"


class GeneratedPrompt(models.Model):
    """The ML-generated prompt corresponding to a UserInput."""

    input_reference  = models.OneToOneField(
        UserInput,
        on_delete=models.CASCADE,
        related_name='generated_prompt',
        verbose_name="Source Input",
    )
    prompt_text      = models.TextField(verbose_name="Generated Prompt")
    tone             = models.CharField(
        max_length=20,
        choices=TONE_CHOICES,
        verbose_name="Detected Tone",
    )
    confidence_score = models.FloatField(
        verbose_name="Confidence Score",
        help_text="Classifier confidence (0–1).",
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    timestamp        = models.DateTimeField(auto_now_add=True, verbose_name="Generated At")

    class Meta:
        ordering         = ['-timestamp']
        verbose_name     = 'Generated Prompt'
        verbose_name_plural = 'Generated Prompts'

    def __str__(self):
        return f"Prompt for [{self.input_reference.category}] – {self.confidence_score:.1%}"

    @property
    def confidence_pct(self):
        return f"{self.confidence_score:.1%}"


class Feedback(models.Model):
    """Optional user feedback on a generated prompt."""

    generated_prompt = models.OneToOneField(
        GeneratedPrompt,
        on_delete=models.CASCADE,
        related_name='feedback',
        verbose_name="Generated Prompt",
    )
    rating           = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name="Rating (1–5)",
    )
    comment          = models.TextField(
        blank=True,
        verbose_name="Comment",
        help_text="Optional written feedback.",
    )
    timestamp        = models.DateTimeField(auto_now_add=True, verbose_name="Submitted At")

    class Meta:
        ordering         = ['-timestamp']
        verbose_name     = 'Feedback'
        verbose_name_plural = 'Feedback'

    def __str__(self):
        return f"⭐ {self.rating}/5 for prompt #{self.generated_prompt.pk}"
