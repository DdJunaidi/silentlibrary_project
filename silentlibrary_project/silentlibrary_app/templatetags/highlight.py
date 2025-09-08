from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight(text, term):
    """
    Wraps occurrences of `term` in <mark>...</mark> (case-insensitive).
    Returns original text if term is empty.
    """
    if not text or not term:
        return text
    try:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
    except re.error:
        return text
    highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", str(text))
    return mark_safe(highlighted)  # so you don't need |safe in templates
