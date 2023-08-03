
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/<str:username>', views.load_profile, name='profile'),
    path('followed_users', views.followed, name='followed'),
    path('cs50w', views.load_cs50w, name='cs50w'),
    

    #API
    path('submit_post', views.submit_post, name='submit_post'),
    path('update_likes', views.update_likes, name='update_likes'),
    path('follow', views.follow, name='follow'),
    path('edit', views.edit, name='edit'),
    path('save', views.save, name='save'),
]
