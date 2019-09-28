from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.Home.as_view(), name="list"),
    path('create/', views.Upload.as_view(), name="create"),
    path('<slug:slug>', views.Meme.as_view(), name="detail"),

]