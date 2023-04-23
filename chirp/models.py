from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', null=True)
    caption = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_rechirps = models.IntegerField(default=0)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.user.username
    
class FollowerCount(models.Model):
    follower = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username  

class Rechirp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='reposted_post', on_delete=models.CASCADE) 

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    parent = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="child_comments", null=True, blank=True)
    body = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user.username       