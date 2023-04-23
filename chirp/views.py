from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Post, LikePost, FollowerCount, Rechirp, Comment
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
from .forms import CommentForm

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    rechirps = Rechirp.objects.filter(user=request.user)
    form = CommentForm()
    

    user_following_list = []
    feed = []
    rechirps = []


    user_following = request.user.followings.all()

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists) 
    
    for usernames in user_following_list:
        rechirps_lists = Rechirp.objects.filter(user=usernames)
        rechirps.append(rechirps_lists) 
           

    feed_list = list(chain(*feed))  
    rechirps_list = list(chain(*rechirps))    

    #user suggestion starts 
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))     


    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4], 'rechirp': rechirps_list, 'form': form})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, user=request.user).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, user=request.user)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def rechirp(request):  
    post_id = request.GET.get('post_id')

    repost = Post.objects.get(id=post_id)

    rechirp_filter = Rechirp.objects.filter(post_id=post_id, user=request.user).first()

    if rechirp_filter == None:
        new_rechirp = Rechirp.objects.create(post_id=post_id, user=request.user)
        new_rechirp.save()
        repost.no_of_rechirps = repost.no_of_rechirps+1
        repost.save()
        return redirect('/')
    else:
        rechirp_filter.delete()
        repost.no_of_rechirps = repost.no_of_rechirps-1
        repost.save()
        return redirect('/')

@login_required(login_url='signin')
def comment(request):
    form = CommentForm()
    
    comments = Comment.objects.filter(post_id=request.GET.get('post_id'))
        

    if request.method == 'POST':
        post = Post.objects.get(id=request.GET.get('post_id'))
        data = request.POST.copy()
        data.update({'post': request.GET.get('post_id'), 'user': request.user})
        form = CommentForm(data)
        if form.is_valid():
            form.save()
            post.no_of_comments += 1
            post.save()         
            return redirect('/')
    
    context = {
        'form': form,
        'comments': comments
    }

    return render(request, 'comment.html', context)
    


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)   
            username_profile_list.append(profile_lists) 

        username_profile_list = list(chain(*username_profile_list))    
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST['user'])

        if FollowerCount.objects.filter(follower=request.user, user=user).first():
            FollowerCount.objects.filter(follower=request.user, user=user).delete()
            return redirect('/profile/'+user.username)
        else:
            FollowerCount.objects.create(follower=request.user, user=user)
            return redirect('/profile/'+user.username)
    else:
        return redirect('/')
    
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=user_object)
    user_post_length = len(user_post)

    follower = request.user
    user = pk

    if FollowerCount.objects.filter(follower=request.user, user=user_object).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'    

    user_followers = len(FollowerCount.objects.filter(user=user_object))
    user_following = len(FollowerCount.objects.filter(follower=request.user))


    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_post' : user_post,
        'user_post_length' : user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')        
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):


    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Is Already In Use')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id) 
                new_profile.save()
                return redirect ('settings')
        else:
            messages.info(request, 'Password Not Correlating')
            return redirect('signup')
    else: 
        return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else: 
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')    
def logout(request):
    auth.logout(request)
    return redirect('signin')