import django_filters

from news_service.models import News, Tag


class NewsFilter(django_filters.FilterSet):
    """
    Фильтр для новостей.
    """
    source = django_filters.CharFilter()
    pub_date = django_filters.DateFromToRangeFilter()
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__name',
        to_field_name='name',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = News
        fields = ['source', 'pub_date', 'tags']