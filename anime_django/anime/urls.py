from django.urls import path

from .views import SingupView, IndexView, LoginView, AnimeDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('animes/<slug:slug>/', AnimeDetailView.as_view(), name='detail'),
    path('singup/', SingupView.as_view(), name='singup'),
    path('login/', LoginView.as_view(), name='login'),
]
