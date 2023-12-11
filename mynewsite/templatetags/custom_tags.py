import datetime

from django import template

from mynewsite.models import Category

register = template.Library()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.inclusion_tag('category.html')
def show_categories():
    categories=Category.objects.all()
    return {"categories": categories}