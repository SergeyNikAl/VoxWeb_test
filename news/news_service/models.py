import uuid
from datetime import datetime
from django.db import models

TEXT_SCOPE = 15
MAX_LENGTH_TAG_NAME = 100
MAX_LENGTH_TAG_SLUG = 100
YANDEX = 'Yandex'
OZON = 'Ozon'
SOURCE = [
    (YANDEX, 'Яндекс'),
    (OZON, 'Озон')
]


class Tag(models.Model):
    uid = models.fields.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    name = models.CharField(
        'Тэг',
        max_length=MAX_LENGTH_TAG_NAME,
        unique=True,
    )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name[:TEXT_SCOPE]


class News(models.Model):
    uid = models.fields.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    title = models.TextField(
        'Заголовок',
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    url = models.URLField(
        'Ссылка',
        null=True,
        unique=True
    )
    source = models.TextField(
        'Сервис',
        max_length=max(len(source) for source, _ in SOURCE),
        choices=SOURCE,
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='news',
    )
    pub_date = models.DateField(
        'Дата публикации',
        default=datetime.now
    )

    class Meta:
        ordering = ['title', ]
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title[:TEXT_SCOPE]
