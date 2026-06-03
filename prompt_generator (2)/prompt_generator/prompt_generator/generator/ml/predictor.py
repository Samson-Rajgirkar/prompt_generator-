"""
predictor.py – Wraps the trained pipeline for inference and prompt generation.

Public API:
    classify(text)  →  PredictionResult(category, confidence, tone, prompt)
"""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field
from typing import Dict, List

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy-loaded pipeline (loaded once on first call)
# ---------------------------------------------------------------------------
_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        from generator.ml.train import load_or_train
        _pipeline = load_or_train()
    return _pipeline


# ---------------------------------------------------------------------------
# Prompt templates per category
# ---------------------------------------------------------------------------
PROMPT_TEMPLATES: Dict[str, List[str]] = {
    "creative": [
        "Act as a world-class creative writer. {action} Write with vivid imagery, "
        "emotional depth, and a compelling narrative arc. Include sensory details "
        "and make every word count.",

        "You are an imaginative storyteller with decades of experience. {action} "
        "Craft your response with originality, rich characters, and an unforgettable "
        "voice that resonates with readers.",

        "Channel your inner author. {action} Focus on atmosphere, tension, and "
        "character motivation. Your writing should be engaging from the first sentence.",
    ],
    "technical": [
        "You are a senior software engineer with deep expertise. {action} Provide "
        "a clear, well-structured solution with code examples, edge case handling, "
        "and best-practice recommendations. Explain your reasoning step by step.",

        "Act as a technical expert and architect. {action} Break down the problem "
        "methodically, consider performance implications, and suggest scalable "
        "approaches with concrete implementation details.",

        "You are a staff engineer reviewing production code. {action} Provide "
        "comprehensive guidance including potential pitfalls, testing strategies, "
        "and industry-standard patterns.",
    ],
    "analytical": [
        "You are a data scientist and critical thinker. {action} Analyse the topic "
        "systematically: identify key variables, examine evidence, consider "
        "alternative explanations, and draw well-reasoned conclusions.",

        "Act as a research analyst. {action} Structure your analysis with clear "
        "sections: context, data interpretation, insights, and actionable "
        "recommendations. Cite logical reasoning throughout.",

        "You are an expert in quantitative and qualitative analysis. {action} "
        "Apply rigorous thinking, challenge assumptions, and present findings "
        "in a clear, evidence-based manner.",
    ],
    "educational": [
        "You are an expert teacher who excels at making complex topics accessible. "
        "{action} Use the Feynman technique: explain as if to a curious beginner, "
        "use relatable analogies, and build understanding step by step.",

        "Act as a patient and knowledgeable tutor. {action} Start with the "
        "fundamentals, use concrete examples, and check understanding at each "
        "stage. Anticipate common misconceptions.",

        "You are an award-winning educator. {action} Make the content engaging "
        "and memorable. Use stories, visual descriptions, and real-world "
        "applications to illuminate the concept.",
    ],
    "business": [
        "You are a seasoned business strategist and consultant. {action} Provide "
        "a professional, results-oriented response. Consider ROI, stakeholder "
        "impact, and market dynamics. Be concise yet comprehensive.",

        "Act as a C-suite executive advisor. {action} Frame your response around "
        "business value, competitive advantage, and measurable outcomes. Use "
        "industry-standard frameworks where appropriate.",

        "You are a growth-focused entrepreneur with a proven track record. {action} "
        "Provide actionable, data-driven guidance that balances ambition with "
        "pragmatism. Include specific next steps.",
    ],
    "conversational": [
        "You are a thoughtful, empathetic conversationalist. {action} Respond "
        "warmly and authentically. Be helpful, honest, and personable—like advice "
        "from a knowledgeable friend.",

        "Act as a trusted advisor and good listener. {action} Consider the "
        "human element, offer balanced perspectives, and personalise your "
        "response to the context provided.",

        "You are insightful and approachable. {action} Keep your tone natural "
        "and engaging. Offer practical wisdom with a friendly, encouraging energy.",
    ],
}

# ---------------------------------------------------------------------------
# Tone modifiers appended to the base prompt
# ---------------------------------------------------------------------------
TONE_MODIFIERS: Dict[str, str] = {
    "formal":     " Maintain a formal, professional tone throughout.",
    "casual":     " Keep the tone friendly, casual, and conversational.",
    "detailed":   " Be thorough and comprehensive—leave nothing out.",
    "concise":    " Be concise and direct. Avoid unnecessary filler.",
    "creative":   " Infuse creativity and originality into every sentence.",
    "technical":  " Use precise technical language appropriate for experts.",
    "persuasive": " Write persuasively—use compelling arguments and rhetorical skill.",
    "simple":     " Use simple, plain language accessible to a general audience.",
}

# ---------------------------------------------------------------------------
# Inferred tone from keywords (lightweight rule-based detection)
# ---------------------------------------------------------------------------
TONE_KEYWORDS: Dict[str, List[str]] = {
    "formal":     ["professional", "formal", "official", "corporate", "proper"],
    "casual":     ["casual", "friendly", "chill", "informal", "relaxed"],
    "detailed":   ["detailed", "thorough", "comprehensive", "in-depth", "exhaustive"],
    "concise":    ["short", "brief", "quick", "concise", "summarize", "tldr"],
    "creative":   ["creative", "imaginative", "artistic", "unique", "original"],
    "technical":  ["technical", "precise", "engineering", "code", "algorithm"],
    "persuasive": ["persuade", "convince", "argue", "pitch", "sell"],
    "simple":     ["simple", "easy", "beginner", "basic", "explain"],
}

# ---------------------------------------------------------------------------
# High-precision intent overrides for common misclassification patterns
# ---------------------------------------------------------------------------
INTENT_OVERRIDE_KEYWORDS: Dict[str, List[str]] = {
    "technical": [
        "python", "javascript", "java", "sql", "api", "bug", "debug",
        "error", "exception", "traceback", "function", "code", "runtimeerror",
        "stack trace", "async", "django", "react",
    ],
    "educational": [
        "routine", "diet", "nutrition", "workout", "exercise", "fitness",
        "gain weight", "lose weight", "muscle", "protein", "calories",
        "meal plan", "training plan", "body weight", "kg", "health",
    ],
}


def detect_intent_override(text: str) -> str | None:
    """Return a high-confidence category override for specific keyword groups."""
    text_lower = text.lower()

    # Prioritize technical terms over general educational terms.
    for category in ("technical", "educational"):
        keywords = INTENT_OVERRIDE_KEYWORDS.get(category, [])
        if any(keyword in text_lower for keyword in keywords):
            return category

    return None


def detect_tone(text: str) -> str:
    """Detect tone from keyword presence; default to 'detailed'."""
    text_lower = text.lower()
    for tone, keywords in TONE_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return tone
    return "detailed"


def _extract_action(text: str) -> str:
    """
    Convert the user's raw input into a clean imperative action phrase.
    Strips conversational wrappers ('can you', 'help me', 'I want to')
    but preserves the core verb + object.
    """
    text = text.strip()

    # Strip conversational openers but NOT action verbs
    openers = [
        r'^please\s+',
        r'^can\s+you\s+',
        r'^could\s+you\s+',
        r'^would\s+you\s+',
        r'^help\s+me\s+(to\s+)?',
        r'^i\s+want\s+you\s+to\s+',
        r'^i\s+want\s+to\s+',
        r'^i\s+need\s+you\s+to\s+',
        r'^i\s+need\s+to\s+',
        r'^i\s+need\s+(a\s+|an\s+)?',
        r'^give\s+me\s+(a\s+|an\s+)?',
    ]

    cleaned = text
    for pattern in openers:
        new = re.sub(pattern, '', cleaned, count=1, flags=re.IGNORECASE).strip()
        if new:
            cleaned = new

    # Ensure sentence ends with punctuation
    if cleaned and cleaned[-1] not in '.!?':
        cleaned += '.'

    # Capitalise first letter
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]

    return cleaned or text + '.'


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------
@dataclass
class PredictionResult:
    category: str
    confidence: float           # 0–1
    tone: str
    generated_prompt: str
    all_probabilities: Dict[str, float] = field(default_factory=dict)

    @property
    def confidence_pct(self) -> str:
        return f"{self.confidence:.1%}"


# ---------------------------------------------------------------------------
# Main classify function
# ---------------------------------------------------------------------------
def classify(text: str) -> PredictionResult:
    """
    Classify the user's text and return a PredictionResult.

    Parameters
    ----------
    text : str
        Raw user input.

    Returns
    -------
    PredictionResult
        Includes category, confidence, tone, and the generated prompt.
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    pipeline = _get_pipeline()

    # ── Predict category ────────────────────────────────────────────────────
    category    = pipeline.predict([text])[0]
    proba_array = pipeline.predict_proba([text])[0]
    classes     = pipeline.classes_
    all_proba   = {cls: float(prob) for cls, prob in zip(classes, proba_array)}

    # Rule-based override for known edge cases where statistical model can drift.
    override_category = detect_intent_override(text)
    if override_category is not None and override_category in all_proba:
        category = override_category
        confidence = max(float(all_proba[category]), 0.80)
    else:
        confidence = float(all_proba[category])

    # ── Detect tone ─────────────────────────────────────────────────────────
    tone = detect_tone(text)

    # ── Build prompt ────────────────────────────────────────────────────────
    import random
    templates    = PROMPT_TEMPLATES.get(category, PROMPT_TEMPLATES["conversational"])
    base_template = random.choice(templates)

    action       = _extract_action(text)
    base_prompt  = base_template.format(action=action)
    tone_suffix  = TONE_MODIFIERS.get(tone, "")
    final_prompt = base_prompt + tone_suffix

    return PredictionResult(
        category=category,
        confidence=confidence,
        tone=tone,
        generated_prompt=final_prompt,
        all_probabilities=all_proba,
    )
