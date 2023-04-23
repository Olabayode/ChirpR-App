from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('upload', views.upload, name= 'upload'),
    path('like-post', views.like_post, name= 'like-post'),
    path('profile/<str:pk>', views.profile, name= 'profile'),
    path('follow', views.follow, name= 'follow'),
    path('rechirp', views.rechirp, name= 'rechirp'),
    path('comment', views.comment, name='comment'),
    path('search', views.search, name= 'search'),
    path('settings', views.settings, name= 'settings'),
    path('signup/', views.signup, name= 'signup'),
    path('signin', views.signin, name= 'signin'),
    path('logout', views.logout, name= 'logout'),
]