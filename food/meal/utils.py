from django.core.cache import cache
from django.db.models import Count, Q

from .models import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = (Category.objects.annotate(food__count=Count('food', filter=Q(food__is_published=True)))
                    .filter(food__count__gt=0))
            cache.set('cats', cats, 60)
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        context['cats'] = cats
        context['cat_selected'] = context.get('cat_selected', 0)

        return context
