from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from posts.models import Posts
from django.views import View
from .forms import UserRegister


class Register(View):
    def get(self, request):
        form = UserRegister()
        return render(request, 'accounts/signup.html', {'form': form})
    def post(self, request):
        form = UserRegister(request.POST)
        if form.is_valid():
            form.cleaned_data.get("email")
            form.cleaned_data.get("username")
            passwordvalue1 = form.cleaned_data.get("password1")
            passwordvalue2 = form.cleaned_data.get("password2")
            if passwordvalue1 == passwordvalue2:
                user = form.save()
                login(request, user)
                return redirect('posts:list')
            else:
                context = {'form': form, 'error': 'The passwords that you provided don\'t match'}
                return render(request, 'accounts/signup.html', context)

        else:
            context = {'form': form}
            return render(request, 'accounts/signup.html', context)


class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            form.cleaned_data.get("username")
            form.cleaned_data.get("password")
            login(request, user)
            return redirect('posts:list')
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form, 'error': 'The passwords that you provided don\'t match'})




class Logout(View):
    def post(self, request):
        logout(request)
        return redirect('posts:list')


class UserView(View):
    def get(self, request, username):
        user_posts = Posts.objects.filter(author__username=username)
        context = {
            'posts': user_posts.all(),
        }
        return render(request, 'accounts/user.html', context=context)