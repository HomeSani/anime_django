from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse

from .forms import SingupUserForm, LoginUserForm


class IndexView(View):
    def get(self, request):
        return render(request, 'anime/index.html', {'user': request.user})


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
