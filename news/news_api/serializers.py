from rest_framework import serializers

from news_service.models import Tag, News


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тэгов.
    """

    class Meta:
        model = Tag
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения новостей
    """

    class Meta:
        model = News
        fields = (
            'uid', 'title', 'description', 'url', 'source', 'tags', 'pub_date'
        )
