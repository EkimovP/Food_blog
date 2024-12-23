from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content', 'author__username')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'author')
    prepopulated_fields = {"slug": ('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'author', 'is_published', 'time_create',
              'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50 height=50>")

    get_html_photo.short_description = "Минифото"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ('name',)}


admin.site.register(Food, FoodAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Сайт о блюдах'
admin.site.site_header = 'Админ-панель сайта о блюдах'
