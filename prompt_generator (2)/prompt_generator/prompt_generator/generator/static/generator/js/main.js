/**
 * main.js – PromptForge frontend interactions
 *
 * Features:
 *   - Character counter for textarea
 *   - Category pill selection
 *   - Submit spinner
 *   - Probability bar animation (triggered on load)
 *   - Copy-to-clipboard for generated prompt
 *   - Star rating selection + feedback form reveal
 *   - Feedback AJAX submission
 *   - Scroll to result
 */

'use strict';

/* ── Helpers ──────────────────────────────────────────────────────────────── */
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

/* ── Character counter ────────────────────────────────────────────────────── */
function initCharCounter() {
  const textarea = $('#input-text');
  const counter  = $('#char-counter');
  if (!textarea || !counter) return;

  const MAX = 1000;

  const update = () => {
    const len = textarea.value.length;
    counter.textContent = `${len} / ${MAX}`;
    counter.classList.toggle('near-limit', len > MAX * 0.8 && len <= MAX);
    counter.classList.toggle('at-limit', len > MAX);
  };

  textarea.addEventListener('input', update);
  update(); // initialise
}

/* ── Hint pills ───────────────────────────────────────────────────────────── */
function initHintPills() {
  const textarea = $('#input-text');
  const selectedCategory = $('#selected-category');
  const pills = $$('.hint-pill');
  if (!textarea) return;

  const setActivePill = (pill) => {
    pills.forEach(item => item.classList.toggle('is-selected', item === pill));
  };

  if (selectedCategory && selectedCategory.value) {
    const active = pills.find(pill => pill.dataset.category === selectedCategory.value);
    if (active) {
      setActivePill(active);
    }
  }

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      if (selectedCategory) {
        selectedCategory.value = pill.dataset.category || '';
      }
      setActivePill(pill);
      textarea.focus();
    });
  });
}

/* ── Submit spinner ───────────────────────────────────────────────────────── */
function initSubmitSpinner() {
  const form = $('#prompt-form');
  const btn  = $('#submit-btn');
  if (!form || !btn) return;

  form.addEventListener('submit', () => {
    btn.classList.add('loading');
    btn.disabled = true;
  });
}

/* ── Probability bar animation ────────────────────────────────────────────── */
function initProbaBars() {
  const fills = $$('.proba-bar-fill');
  if (!fills.length) return;

  // Use requestAnimationFrame so CSS transitions trigger after paint
  requestAnimationFrame(() => {
    fills.forEach(bar => {
      const target = parseFloat(bar.dataset.width || 0) * 100;
      bar.style.width = Math.min(target, 100) + '%';
    });
  });
}

/* ── Copy to clipboard ────────────────────────────────────────────────────── */
function initCopyButton() {
  const btn = $('#copy-btn');
  if (!btn) return;

  btn.addEventListener('click', async () => {
    const targetId = btn.dataset.target;
    const el = targetId ? document.getElementById(targetId) : null;
    const text = el ? el.textContent.trim() : '';

    try {
      await navigator.clipboard.writeText(text);
      const label = btn.querySelector('.copy-label');
      btn.classList.add('copied');
      if (label) label.textContent = 'Copied!';
      setTimeout(() => {
        btn.classList.remove('copied');
        if (label) label.textContent = 'Copy';
      }, 2000);
    } catch {
      // Fallback for older browsers
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
  });
}

/* ── Star rating ──────────────────────────────────────────────────────────── */
function initStarRating() {
  const starRow      = $('#star-row');
  const feedbackForm = $('#feedback-form');
  if (!starRow || !feedbackForm) return;

  const stars   = $$('.star-btn', starRow);
  const ratingInput = feedbackForm.querySelector('input[name="rating"]') ||
                      feedbackForm.querySelector('select[name="rating"]');

  // Handle radio inputs for rating
  const radioInputs = $$('input[type="radio"][name="rating"]', feedbackForm);

  const setRating = (rating) => {
    stars.forEach((s, i) => {
      s.classList.toggle('active', i < rating);
    });
    // Update the hidden/radio input
    radioInputs.forEach(r => {
      r.checked = (parseInt(r.value) === rating);
    });
    feedbackForm.style.display = 'block';
  };

  stars.forEach((star, idx) => {
    star.addEventListener('mouseover', () => {
      stars.forEach((s, i) => s.classList.toggle('active', i <= idx));
    });
    star.addEventListener('mouseleave', () => {
      // Restore to selected state
      const selected = stars.findIndex(s => s.dataset.rating === (ratingInput && ratingInput.value));
      stars.forEach((s, i) => s.classList.toggle('active', i <= selected));
    });
    star.addEventListener('click', () => {
      setRating(idx + 1);
    });
  });
}

/* ── Feedback AJAX submission ─────────────────────────────────────────────── */
function initFeedbackSubmit() {
  const feedbackForm = $('#feedback-form');
  const thanks       = $('#feedback-thanks');
  if (!feedbackForm || !thanks) return;

  feedbackForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data     = new FormData(feedbackForm);
    const url      = feedbackForm.action;
    const csrfToken = (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || '';

    try {
      const res  = await fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        body: data,
      });
      const json = await res.json();

      if (json.status === 'ok' || json.status === 'already_submitted') {
        feedbackForm.style.display = 'none';
        $('#star-row').style.display = 'none';
        thanks.hidden = false;
      }
    } catch (err) {
      console.error('Feedback submission failed:', err);
    }
  });
}

/* ── Scroll to result ─────────────────────────────────────────────────────── */
function scrollToResult() {
  const result = $('#result-section');
  if (!result) return;

  // Small delay so the page has finished rendering
  setTimeout(() => {
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 150);
}

/* ── Boot ─────────────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initCharCounter();
  initHintPills();
  initSubmitSpinner();
  initProbaBars();
  initCopyButton();
  initStarRating();
  initFeedbackSubmit();
  scrollToResult();
});
