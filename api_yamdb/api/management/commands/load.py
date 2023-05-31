import csv
import logging

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

logging.basicConfig(level=logging.INFO)


def load(model, path, related_models=None,):
    logging.info(f'Загрузка данных в таблицу {model.__name__}')
    model.objects.all().delete()

    with open(path) as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                logging.info(row)

                if related_models:
                    for rel_model in related_models:
                        related_name = rel_model[0]
                        csv_name = rel_model[1]
                        mod = rel_model[2]
                        id = row.pop(csv_name)
                        mod = get_object_or_404(mod, id=id)
                        row[related_name] = mod

                model.objects.create(**row)
            except Exception:
                logging.warning('Ошибка в данных')


class Command(BaseCommand):
    help = 'Загрузка тестовых записей в БД'

    def handle(self, *args, **options):
        load(User, 'static/data/users.csv')
        load(Category, 'static/data/category.csv')
        load(Genre, 'static/data/genre.csv')
        load(Title, 'static/data/titles.csv',
             [('category', 'category', Category), ])
        load(GenreTitle, 'static/data/genre_title.csv')
        load(Review,
             'static/data/review.csv',
             [('title', 'title_id', Title),
              ('author', 'author', User)])
        load(Comment,
             'static/data/comments.csv',
             [('review', 'review_id', Review),
              ('author', 'author', User)])
