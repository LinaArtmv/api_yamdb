# Generated by Django 3.2 on 2023-05-30 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='genretitle',
            constraint=models.UniqueConstraint(fields=('genre', 'title'), name='unique_genre_title_records'),
        ),
    ]
