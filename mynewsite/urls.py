"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .import views
from django.urls import path

urlpatterns = [
    path('single/', views.Single, name='category'),
    path('index/', views.Index, name='index'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('update_blog/<int:pk>', views.update_blog, name='update_blog'),
    path('delete_blog/<int:pk>', views.delete_blog,name='delete_blog'),
    path('single/<int:pk>', views.Single, name='single'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('dislike/<int:pk>/', views.dislike_post, name='dislike_post'),
    path('comment/<int:pk>/', views.post_comments, name='post_comment'),
    path('signin/', views.Signin.as_view(), name='signin'),
    path('signup/', views.Signup.as_view(), name='signup'),
]
