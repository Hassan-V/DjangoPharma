from django import template
from django.forms.widgets import Widget
import logging

register = template.Library()
logger = logging.getLogger(__name__)

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Appends a CSS class to a Django form field, preserving existing classes.
    """
    if not isinstance(value, Widget):
        logger.error(f"add_class filter applied to a non-Widget value: {value}")
        return value
    existing_classes = value.attrs.get('class', '')
    new_classes = f"{existing_classes} {arg}".strip()
    logger.debug(f"Adding classes '{arg}' to field. New class value: '{new_classes}'")
    return value.as_widget(attrs={"class": new_classes})