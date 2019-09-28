
from django.shortcuts import render, redirect
from .models import Posts, Comments
from .forms import CreatePosts
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(View):
    def get(self, request):
        posts = Posts.objects.all()
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')

        posts = paginator.get_page(page)
        context = {'posts': posts}
        return render(request, 'posts/posts_list.html', context)

class Meme(View):
    def get(self, request, slug):
        post = Posts.objects.get(slug=slug)
        context = {
            'post': post,
            'comments': post.comments_set.all(),
        }
        return render(request, 'posts/posts_detail.html', context)

    def post(self, request, slug):
        post = Posts.objects.get(slug=slug)
        Comments.objects.create(author=request.user, post=post, content=request.POST.get('content', ''))
        return redirect('posts:detail', slug)



class Upload(View, LoginRequiredMixin):
    def get(self, request):
        form = CreatePosts()
        return render(request, 'posts/post_create.html', {'form': form})

    def post(self, request):
        form = CreatePosts(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('posts:list')