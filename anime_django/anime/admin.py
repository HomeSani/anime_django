from django.contrib import admin

from .models import Anime, Gengre, Studio, Episode, Review, Vote, Follow


admin.site.register([Gengre, Studio, Follow])


class EpisodeInline(admin.StackedInline):
    model = Episode


@admin.register(Anime)
class AnimeModelAdmin(admin.ModelAdmin):
    model = Anime
    # Перенос строк ненужный, линтер установи чтобы такое подсказывал
    list_display = ['name',
                    'name_on_japan', 'status', 'image_tag', 'is_featured']
    list_editable = ['is_featured']
    # Запятая
    inlines = [EpisodeInline]


@admin.register(Episode)
class EpisodeModelAdmin(admin.ModelAdmin):
    model = Episode
    # Запятая
    list_display = ['name', 'number', 'anime']


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    model = Review
    # Запятая
    list_display = ['author', 'create_date', 'anime', 'episode']


@admin.register(Vote)
class VoteModelAdmin(admin.ModelAdmin):
    model = Vote
    # Запятая
    list_display = ['user', 'anime', 'count']
