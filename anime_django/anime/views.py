from operator import attrgetter

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse
from django.utils import timezone

from .forms import SingupUserForm, LoginUserForm, ReviewForm, VoteForm, DateFilterForm
from .models import Anime, Review, Vote


class IndexView(View):
    def get(self, request):
        animes = Anime.objects.all()
        featured_animes = list(animes.filter(is_featured=True))
        rated_animes_sorted = list(sorted(
            list(map(lambda anime: (anime.get_rating(anime), anime), animes)), reverse=True))
        rated_animes = list(map(lambda anime: anime[-1], rated_animes_sorted))
        popular_animes = list(animes.order_by('-views'))[:6]
        recently_animes = list(animes.order_by('-add_date'))[:6]
        recently_review_animes = self.get_recently_reviwe_animes(animes=animes)
        range = "year"

        if request.GET.get("range"):
            range = request.GET.get("range")

        animes_views_date_range = self.get_animes_by_views_date_range(range=range)

        return render(request, 'anime/index.html', {'featured_animes': featured_animes, 'rated_animes': rated_animes,
                                                    'popular_animes': popular_animes,
                                                    "recently_animes": recently_animes,
                                                    "recently_review_animes": recently_review_animes,
                                                    "animes_views_date_range": animes_views_date_range})

    def post(self, request):
        form = DateFilterForm(request.POST)

        if form.is_valid():
            range = form.cleaned_data["range"]

            return redirect(reverse("index") + "?range=" + range)

        return redirect(reverse("index"))

    def get_animes_by_views_date_range(self, range='day'):
        animes = self.get_anime_by_date_range(range=range)[:4]

        return list(sorted(animes, key=attrgetter("views")))

    def get_anime_by_date_range(self, range):
        date = str(timezone.now()).split(" ")[0].split("-")
        year = date[0]
        month = date[1]
        day = date[2]

        if range == "day":
            return list(Anime.objects.filter(add_date__day=day))
        if range == "week":
            current_week = timezone.now().isocalendar()[1]
            return list(Anime.objects.filter(release_date__week=current_week))
        elif range == "month":
            return list(Anime.objects.filter(add_date__month=month))
        elif range == "year":
            return list(Anime.objects.filter(add_date__year=year))

        return []

    def get_recently_reviwe_animes(self, animes):
        recently_reviews = []

        for anime in animes:
            reviews = anime.get_rewiews(anime=anime)

            if len(reviews) != 0:
                recently_reviews.append((sorted(map(lambda review: review.create_date, reviews))[-1], anime))
                recently_reviews = sorted(recently_reviews, reverse=True)[:6]
            else:
                recently_reviews = []

        return list(map(lambda review: review[-1], recently_reviews))


class AnimeDetailView(View):
    def get(self, request, slug):
        anime = Anime.objects.get(slug=slug)
        reviews = list(Review.objects.filter(anime=anime))
        last_added_animes = list(Anime.objects.order_by('-add_date')[:5])
        votes = anime.get_votes(anime=anime)
        votes_count = len(votes)
        rating = anime.get_rating(anime=anime)
        user_vote = Vote.objects.filter(
            user=request.user, anime=anime).exists()
        user_vote_count = []

        if user_vote:
            vote = Vote.objects.get(user=request.user, anime=anime)
            user_vote_count = range(vote.count + 1)

        anime.increment_views()

        return render(request, 'anime/detail.html', {
            'anime': anime,
            'user': request.user,
            'reviews': reviews,
            'last_added_animes': last_added_animes,
            'votes_count': votes_count,
            'user_vote_count': user_vote_count,
            'stars_count': range(5),
            'rating': rating
        })

    def post(sefl, request, slug):
        anime = Anime.objects.get(slug=slug)

        review_form = ReviewForm(request.POST)
        vote_form = VoteForm(request.POST)

        if review_form.is_valid():
            review = Review()
            review.author = request.user
            review.anime = anime
            review.text = review_form.cleaned_data['text']

            review.save()

        if vote_form.is_valid():
            vote_is_exist = Vote.objects.filter(
                user=request.user, anime=anime).exists()

            if vote_is_exist:
                vote = Vote.objects.get(
                    user=request.user, anime=anime)
                vote.count = vote_form.cleaned_data['rating']

                vote.save()
            else:
                vote = Vote()
                vote.count = vote_form.cleaned_data['rating']
                vote.anime = anime
                vote.user = request.user

                vote.save()

        return redirect(reverse('detail', args=[anime.slug]))


class SingupView(View):
    def get(self, request):
        return render(request, 'anime/singup.html')

    def post(self, request):
        form = SingupUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse('index'))

        return render(request, 'anime/singup.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'anime/login.html')

    def post(self, request):
        form = LoginUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect(reverse('index'))
            else:
                form.add_error(None, "Invalid username or password.")

        return render(request, 'anime/login.html', {'form': form})
