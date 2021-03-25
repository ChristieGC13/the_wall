from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('post_message/<int:user_id>', views.post_message),
    path('post_comment/<int:user_id>', views.post_comment),
    path('logoff', views.logoff),
]