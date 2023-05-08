import os

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

from .const import RELEASE_TYPES, STATUS


class Gengre(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Gengre, self).save(*args, **kwargs)


class Studio(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Anime(models.Model):
    name = models.CharField(max_length=250)
    name_on_japan = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    slug = models.SlugField(blank=True)
    genre = models.ManyToManyField(Gengre, related_name='genres')
    release_type = models.CharField(choices=RELEASE_TYPES, max_length=64)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    release_date = models.DateTimeField(default=timezone.now)
    add_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=STATUS, max_length=64)
    views = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(
        default=24, verbose_name='Episode duration in minutes')
    poster = models.ImageField(upload_to='posters')
    finish_episode_count = models.PositiveIntegerField(
        default=12, verbose_name="How many episodes are planned")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Anime, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Episode(models.Model):
    name = models.CharField(max_length=128)
    number = models.PositiveIntegerField(
        verbose_name="Which episode is in order")
    anime = models.ForeignKey(
        Anime, on_delete=models.CASCADE, related_name='episodes')
    video = models.FileField(upload_to=f'episodes/')

    def save(self, *args, **kwargs):
        filename = f"{self.anime.name}-{self.number}.{self.video.url.split('.')[-1]}"
        upload_path = f"{self.anime.slug}/"
        self.video.name = os.path.join(upload_path, filename)

        super(Episode, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    create_date = models.DateTimeField(default=timezone.now)
    anime = models.ForeignKey(
        Anime, on_delete=models.CASCADE, null=True, blank=True)
    episode = models.ForeignKey(
        Episode, on_delete=models.CASCADE, null=True, blank=True)


class Vote(models.Model):
    count = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
