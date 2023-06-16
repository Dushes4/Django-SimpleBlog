from django.urls import path

from .views import post, feed, create_post, login_user, logout_user, register_user

urlpatterns = [
    path('', feed),
    path('post/<int:post_id>', post),
    path('create_post/', create_post),
    path('login/', login_user),
    path('logout/', logout_user),
    path('register/', register_user)
]
