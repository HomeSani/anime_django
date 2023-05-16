import os

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html

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
    is_featured = models.BooleanField(default=False)
    image_featured = models.ImageField(
        upload_to='posters', blank=True, default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Anime, self).save(*args, **kwargs)

    def get_votes(self, anime):
        return list(Vote.objects.filter(anime=anime))

    def get_episodes(self, anime):
        return list(Episode.objects.filter(anime=anime))

    def get_rewiews(self, anime):
        return list(Review.objects.filter(anime=anime))

    def get_rating(self, anime):
        votes = self.get_votes(anime=anime)
        votes_count = len(votes)
        rating = 0

        if votes_count != 0:
            rating = round(
                sum(map(lambda vote: vote.count, votes)) / votes_count, 1)

        return rating

    def increment_views(self):
        self.views += 1
        super(Anime, self).save()

    def image_tag(self):
        return format_html('<img src="{}" height="50" />'.format(self.poster.url))

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
    anime = models.ForeignKey(
        Anime, on_delete=models.CASCADE, related_name='animes')


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
