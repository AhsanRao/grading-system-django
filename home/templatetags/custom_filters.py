# custom_filters.py

from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()


@register.filter(name="add_class")
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get("class", "")
    if css_classes:
        css_classes = f"{css_classes} {arg}"
    else:
        css_classes = arg
    return value.as_widget(attrs={"class": css_classes})


@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary.get(key)


# @register.filter(name='is_supervisor_for')
# def is_supervisor_for(user, group_id):
#     return user.is_supervisor_for_group(group_id)

# @register.filter(name='is_examiner_for')
# def is_examiner_for(user, group_id):
#     return user.is_examiner_for_group(group_id)


@register.filter
def is_supervisor_for(user, group_id):
    """Template filter to check if the user is a supervisor for a specific group."""
    return user.is_supervisor_for_group(group_id)


@register.filter
def is_examiner_for(user, group_id):
    """Template filter to check if the user is an examiner for a specific group."""
    return user.is_examiner_for_group(group_id)
