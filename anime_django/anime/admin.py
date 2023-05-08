from django.contrib import admin

from .models import Anime, Gengre, Studio, Episode, Review, Vote, Follow


admin.site.register([Gengre, Studio, Follow])


@admin.register(Anime)
class AnimeModelAdmin(admin.ModelAdmin):
    model = Anime
    list_display = ['name', 'name_on_japan', 'status', 'release_date']


@admin.register(Episode)
class EpisodeModelAdmin(admin.ModelAdmin):
    model = Episode
    list_display = ['name', 'number', 'anime']


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    model = Review
    list_display = ['author', 'create_date', 'anime', 'episode']


@admin.register(Vote)
class VoteModelAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ['user', 'anime', 'count']
