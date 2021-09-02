
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # handmade    
    path("newpost", views.new_post, name="new_post"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("follow/<str:whose_profile>", views.follow, name="follow"),
    path("unfollow/<str:whose_profile>", views.unfollow, name="unfollow"),
    path("following/", views.following, name="following"),
    # api:
    # posts
    path("api_listposts", views.ListPosts.as_view(), name="api_listposts"),
    path("api_detailed_post/<int:pk>/",views.DetailedPostMixins.as_view(), name="productmixin"),
    # likes
    path("api_detailed_like/<int:pk>/",views.LikeMixins.as_view(), name="productmixin"),
    path("api_listlikes", views.ListLikes.as_view(), name="api_listlikes"),
    
]

