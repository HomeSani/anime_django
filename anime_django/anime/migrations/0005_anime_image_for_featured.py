# Generated by Django 4.2.1 on 2023-05-10 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0004_anime_is_featured_alter_anime_release_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='image_for_featured',
            field=models.ImageField(blank=True, default='', upload_to='posters'),
        ),
    ]
