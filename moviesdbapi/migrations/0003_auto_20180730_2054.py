# Generated by Django 2.0.7 on 2018-07-30 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesdbapi', '0002_movie_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
