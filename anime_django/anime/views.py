from functools import reduce

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse

from .forms import SingupUserForm, LoginUserForm, ReviewForm, VoteForm
from .models import Anime, Review, Vote


class IndexView(View):
    def get(self, request):
        return render(request, 'anime/index.html', {'user': request.user})


class AnimeDetailView(View):
    def get(self, request, slug):
        anime = Anime.objects.get(slug=slug)
        reviews = list(Review.objects.filter(anime=anime))
        last_added_animes = list(Anime.objects.order_by('-add_date')[:5])
        votes = list(Vote.objects.filter(anime=anime))
        votes_count = len(votes)
        rating = 0
        user_vote = Vote.objects.filter(
            user=request.user, anime=anime).exists()
        user_vote_count = []

        if votes_count != 0:
            rating = round(
                sum(map(lambda vote: vote.count, votes)) / votes_count, 1)

        if user_vote:
            vote = Vote.objects.get(user=request.user, anime=anime)
            user_vote_count = range(vote.count+1)

        anime.views += 1
        anime.save()

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
