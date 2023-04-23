from django.contrib import admin
from .models import Profile, Post, LikePost, FollowerCount, Rechirp, Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowerCount)
admin.site.register(Rechirp)
admin.site.register(Comment)