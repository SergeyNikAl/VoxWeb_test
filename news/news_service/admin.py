from django.contrib import admin

from .models import News, Tag

EMPTY_VALUE = '-пусто-'

@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ['title', 'url', 'pub_date', 'source', 'get_tags_list']
    list_filter = [
        'pub_date', 'source', ('tags__name', admin.AllValuesFieldListFilter)
    ]
    search_fields = ['title', 'source', ]
    empty_value_display = EMPTY_VALUE


    @admin.display(description='Тэги',)
    def get_tags_list(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ['name', ]
    empty_value_display = EMPTY_VALUE
