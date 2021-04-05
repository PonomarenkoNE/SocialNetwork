from django.shortcuts import render, redirect, reverse
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime
from .forms import RegistrationForm, SignInForm, PostForm
from .models import User, Post, Like, Dislike
from .serializers import LikesAnalyticsSerializer, UserSerializer, PostSerializer, LikeSerializer, DislikeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

TOKEN_URL = settings.TOKEN_URL


def logout_user(request):
    logout(request)
    return redirect(reverse('sign_in'))


def take_data_from_form(form):
    data = dict()
    data['user_email'] = form.cleaned_data['email']
    data['user_password'] = form.cleaned_data['password']
    data['user_name'] = data['user_email'].split('@')[0]
    return data


class RegistrationAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        context = {'form': RegistrationForm}
        return render(request, 'registration.html', context=context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_data = take_data_from_form(form)
            if not User.objects.filter(email=user_data['user_email']):
                username = user_data['user_name']
                email = user_data['user_email']
                password = user_data['user_password']
                new_user = User.objects.create_user(username=username, email=email)
                new_user.set_password(password)
                new_user.save()
                user = authenticate(request, username=username, password=password)
                response = requests.post(TOKEN_URL, data={'username': username, 'password': password})
                data = response.json()
                login(request, user)
                header = {'Authorization': 'Bearer' + data['access']}
                return redirect(reverse('blog'), headers=header)
            else:
                messages.warning(request, 'Account already exists')
                return HttpResponseRedirect(self.request.path_info)


class SignInAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        context = {'form': SignInForm}
        return render(request, 'sign_in.html', context=context)

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user_data = take_data_from_form(form)
            username = user_data['user_name']
            password = user_data['user_password']
            user = authenticate(username=username, password=password)
            if user is not None:
                response = requests.post(TOKEN_URL, data={'username': username, 'password': password})
                data = response.json()
                login(request, user)
                header = {'Authorization': 'Bearer'+ data['access']}
                return redirect(reverse('blog'), headers=header)
            else:
                messages.warning(request, 'Wrong email or password')
                return HttpResponseRedirect(self.request.path_info)


class PostsFeedAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        posts = Post.objects.all().order_by('-date')
        context = {'posts': posts}
        return render(request, 'blog.html', context=context)


class CreatePostAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = {'form': PostForm}
        return render(request, 'add_post.html', context=context)

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_photo = form.cleaned_data['photo']
            post_title = form.cleaned_data['title']
            post_description = form.cleaned_data['description']
            new_post = Post.objects.create(author=request.user, title=post_title,
                                           description=post_description,
                                           date=datetime.now(), photo=post_photo)
            new_post.save()
            return redirect(reverse('blog'))


class LikeAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        current_user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=post_id)
        if not Like.objects.filter(who_liked=current_user, post=post):
            if Dislike.objects.filter(who_disliked=current_user, post=post):
                dislike_to_delete = Dislike.objects.filter(who_disliked=current_user, post=post)
                dislike_to_delete.delete()
                post.unlikes -= 1
                post.save()
            like = Like(who_liked=current_user, post=post, date=datetime.now())
            like.save()
            post.likes += 1
            post.save()
        return Response({"likes_count": post.likes, "dislikes_count": post.unlikes}, status=200)


class DislikeAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        current_user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=post_id)
        if not Dislike.objects.filter(who_disliked=current_user, post=post):
            if Like.objects.filter(who_liked=current_user, post=post):
                like_to_delete = Like.objects.filter(who_liked=current_user, post=post)
                like_to_delete.delete()
                post.likes -= 1
                post.save()
            dislike = Dislike(who_disliked=current_user, post=post, date=datetime.now())
            dislike.save()
            post.unlikes += 1
            post.save()
        return Response({"likes_count": post.likes, "dislikes_count": post.unlikes}, status=200)


class LikesAnalyticsAPI(generics.ListAPIView):
    serializer_class = LikesAnalyticsSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        date_from = datetime.strptime(self.request.GET.get('date_from', None), '%d-%m-%Y').date()
        date_to = datetime.strptime(self.request.GET.get('date_to', None), '%d-%m-%Y').date()
        likes = Like.objects.filter(date__range=[date_from, date_to])
        return likes


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAdminUser]


class DislikeViewSet(viewsets.ModelViewSet):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permission_classes = [IsAdminUser]

