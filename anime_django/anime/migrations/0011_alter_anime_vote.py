# Generated by Django 4.2.1 on 2023-05-10 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0010_remove_anime_vote_anime_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='vote',
            field=models.ManyToManyField(related_name='votes', to='anime.vote'),
        ),
    ]
