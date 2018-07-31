# Generated by Django 2.0.7 on 2018-07-31 17:38

from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
        ('moviesdbapi', '0003_auto_20180730_2054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=255)),
                ('movie', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='movie', to='moviesdbapi.Movie')),
            ],
        ),
    ]
