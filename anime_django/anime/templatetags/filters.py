from django import template


register = template.Library()


@register.filter()
def get_rewiews_count(anime):
    return len(anime.get_rewiews(anime=anime))
