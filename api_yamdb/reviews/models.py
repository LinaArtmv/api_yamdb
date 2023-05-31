import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


NUMBER_OF_SYMBOLS = 15


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:NUMBER_OF_SYMBOLS]


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:NUMBER_OF_SYMBOLS]


class Title(models.Model):
    """Модель произведений."""

    name = models.TextField(max_length=256, verbose_name='Название')
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        through='GenreTitle'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True)
    year = models.PositiveIntegerField(
        verbose_name='Год создания',
        validators=[MaxValueValidator(dt.datetime.now().year)]
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:NUMBER_OF_SYMBOLS]


class GenreTitle(models.Model):
    """Связующая модель для жанров и произведений."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(verbose_name='Отзыв')
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')
        ]

    def __str__(self):
        return self.text[:NUMBER_OF_SYMBOLS]


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text[:NUMBER_OF_SYMBOLS]
