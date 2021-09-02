from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# https://stackoverflow.com/questions/65215732/conditionally-calling-str-in-models-py-in-accordance-to-the-related-name-d
class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, through='Follow', related_name='followees', through_fields=('followee', 'follower'))
    image = models.CharField(max_length=1000, default='https://bit.ly/3jmr8Jl', null=True)
    about = models.CharField(max_length=400, blank=True,null=True, default='')
    
    
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='followedby', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.follower} follows {self.followee}'


class Post(models.Model):    
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.CharField(max_length=1000)
    post_pub_date = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return f"{self.post_author}"


class Like(models.Model):
    post_id = models.ForeignKey(Post, related_name='post_id_like', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name='user_id_like', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"post:{self.post_id} like by {self.user_id}"



