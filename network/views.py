from network.serializer import PostSerializer, LikeSerializer
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow, Like
from .forms import PostModelForm, UserProfileForm

from rest_framework import mixins
from rest_framework import generics


PAGINATION_PAGES = 10


@login_required(login_url="/accounts/login/")
def index(request):    
    # pagination, and showing posts
    posts = Post.objects.get_queryset().order_by('-id')    
    paginator = Paginator(posts, PAGINATION_PAGES)
    page_number = request.GET.get('page')    
    page_obj = paginator.get_page(page_number)   
    
    form_profile = UserProfileForm()
    

    # this is the list of !id's of the posts! which YOUR user liked
    like_obj = Like.objects.filter(user_id=request.user)   
    like_list = []
    for like in like_obj:
        id = like.post_id.id
        like_list.append(id)
    #print(like_list)
        
    like = Like.objects.all()
        
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        'form_profile': form_profile,
        "like_list": like_list,
        "like":like,
    })
    
    
def following(request):
    user = request.user
    # returns queryset of follow objects wher your user is folower
    follows_obj = Follow.objects.filter(follower=user)          
    
    # https://stackoverflow.com/questions/29587382/how-to-add-an-model-instance-to-a-django-queryset/43544410
    # this returns all users who you are following
    users_list = User.objects.none()
    for i in follows_obj:
        instance = i.followee
        users_list |= User.objects.filter(pk=instance.pk)
        
    # this returns queryset of all posts which has "post_author=user" in users_list above
    post_list = Post.objects.none()
    for i in users_list:
        instance = i        
        post_list |= Post.objects.filter(post_author=instance.pk).order_by('-id')
        
    #posts to render on following page    
    posts = post_list    
    paginator = Paginator(posts, PAGINATION_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form_profile = UserProfileForm()
    
    # this is the list of !id's of the posts! which YOUR user liked
    like_obj = Like.objects.filter(user_id=request.user)
    like_list = []
    for like in like_obj:
        id = like.post_id.id
        like_list.append(id)
    #print(like_list)

    like = Like.objects.all()

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        'form_profile': form_profile,
        "like_list": like_list,
        "like": like,
    })


def follow(request, whose_profile):
    id_of_folower = User.objects.get(username=request.user)
    id_of_folowee = User.objects.get(username=whose_profile)
    
    if request.method == "POST":    
        new_follow = Follow.objects.create(follower=id_of_folower, followee=id_of_folowee)
        new_follow.save()
        return HttpResponseRedirect(reverse("profile", args=[whose_profile]))


def unfollow(request, whose_profile):
    id_of_folower = User.objects.get(username=request.user)
    id_of_folowee = User.objects.get(username=whose_profile)

    if request.method == "POST":
        find_follow = Follow.objects.filter(follower=id_of_folower, followee=id_of_folowee).first()
        find_follow.delete()
        return HttpResponseRedirect(reverse("profile", args=[whose_profile]))


def profile(request, user):
    if request.method == "GET":
        #actual loggined user
        id_of_user = User.objects.get(username=user)    
        #user whose profile you in
        followee_id = User.objects.get(username=request.user)  
        posts = Post.objects.filter(post_author=id_of_user).order_by('-id')  
        
        paginator = Paginator(posts, PAGINATION_PAGES)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
            
        how_many_followers = Follow.objects.filter(followee=id_of_user).count()    
        how_many_follows = Follow.objects.filter(follower=id_of_user).count() 
        how_many_posts = Post.objects.filter(post_author=id_of_user).count()
        
        #check if it is users own profile and turn follow button off:
        users_profile = False
        if followee_id == id_of_user:
            users_profile = True
        
        #check if user follows other user or not    
        follow_bool = False
        check = Follow.objects.filter(followee=id_of_user, follower=followee_id).count()
        if check > 0:
            follow_bool=True 
        
        form_profile = UserProfileForm()
        return render(request, "network/profile.html", {
            "posts": page_obj,        
            "id_of_user": id_of_user,
            "how_many_followers": how_many_followers,
            "how_many_follows": how_many_follows,
            "users_profile": users_profile,
            "follow_bool": follow_bool,
            "how_many_posts": how_many_posts,
            "form_profile": form_profile,
        })
    elif request.method == "POST":        
        form_profile = UserProfileForm(request.POST)
        
        if form_profile.is_valid():            
            user = request.user
            user.image = form_profile.cleaned_data['image']
            user.about = form_profile.cleaned_data['about']
            user.save()            
            return HttpResponseRedirect(reverse("profile", args=[user]))
        
def new_post(request):
    if request.method == "POST":
        from_new_post = PostModelForm(request.POST)        
        if from_new_post.is_valid():
            post_author = request.user
            post_text = from_new_post.cleaned_data['post_text']
            
            new_post = Post(post_author=post_author, post_text=post_text)
            new_post.save()
            
        #return render(request, "network/new_post.html")
        return HttpResponseRedirect(reverse("index"))
    else:
        from_new_post = PostModelForm()
        return render(request, "network/new_post.html", {
            "from_new_post": from_new_post,
        })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# serializers - api

class ListPosts(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DetailedPostMixins(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView,):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ListLikes(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LikeMixins(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView,):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
