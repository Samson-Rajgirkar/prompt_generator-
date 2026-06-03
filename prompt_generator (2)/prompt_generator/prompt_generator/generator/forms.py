"""
forms.py – Django forms for input validation.
"""

from django import forms
from .models import Feedback


class PromptInputForm(forms.Form):
    """Main form: user enters text to generate a prompt."""

    input_text = forms.CharField(
        label="",
        min_length=5,
        max_length=1000,
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe what you need help with… e.g. "Write a short story about a robot discovering emotions"',
            'rows': 4,
            'class': 'input-textarea',
            'id': 'input-text',
            'autofocus': True,
        }),
        error_messages={
            'required':  'Please enter some text.',
            'min_length': 'Please enter at least 5 characters.',
            'max_length': 'Please keep your input under 1 000 characters.',
        },
    )


class FeedbackForm(forms.ModelForm):
    """Feedback form: rate and comment on a generated prompt."""

    class Meta:
        model   = Feedback
        fields  = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'star-radio'}),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Any additional feedback? (optional)',
                'rows': 3,
                'class': 'feedback-textarea',
            }),
        }
        labels = {
            'rating':  'Rate this prompt',
            'comment': 'Comment',
        }
