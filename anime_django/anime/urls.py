from django.urls import path

from .views import SingupView, IndexView, LoginView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('singup/', SingupView.as_view(), name='singup'),
    path('login/', LoginView.as_view(), name='login'),
]
