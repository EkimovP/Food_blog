from django import template

from meal.models import *


register = template.Library()


@register.inclusion_tag('meal/leftmenu.html')
def left_menu(extra_links=None):
    context_left_menu = [
        {'title': 'Назад на главную', 'url': reverse('home')},
    ]

    if extra_links:
        context_left_menu.extend(extra_links)

    return {'left_menu': context_left_menu}
