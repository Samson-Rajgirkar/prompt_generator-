"""Admin configuration for the generator app."""

from django.contrib import admin
from .models import UserInput, GeneratedPrompt, Feedback


@admin.register(UserInput)
class UserInputAdmin(admin.ModelAdmin):
    list_display  = ('id', 'category', 'short_text', 'timestamp')
    list_filter   = ('category', 'timestamp')
    search_fields = ('input_text',)
    ordering      = ('-timestamp',)

    def short_text(self, obj):
        return obj.input_text[:80]
    short_text.short_description = 'Input Text'


@admin.register(GeneratedPrompt)
class GeneratedPromptAdmin(admin.ModelAdmin):
    list_display  = ('id', 'get_category', 'tone', 'confidence_pct', 'timestamp')
    list_filter   = ('tone', 'timestamp')
    ordering      = ('-timestamp',)

    def get_category(self, obj):
        return obj.input_reference.category
    get_category.short_description = 'Category'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'rating', 'short_comment', 'timestamp')
    list_filter  = ('rating', 'timestamp')

    def short_comment(self, obj):
        return obj.comment[:60] if obj.comment else '—'
    short_comment.short_description = 'Comment'
