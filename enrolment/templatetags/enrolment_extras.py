from django import template
from django.forms import BoundField

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def add_class(value, arg):
    """Add CSS classes to a form field widget."""
    if isinstance(value, BoundField):
        return value.as_widget(attrs={"class": arg})
    return value
