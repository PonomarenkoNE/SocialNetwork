from rest_framework import serializers
from .models import User, Like, Dislike, Post


class LikesAnalyticsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Like
        fields = ('who_liked', 'post', 'date')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_login', 'date_joined']


class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Post
        fields = ['url', 'author', 'title', 'description', 'date', 'likes', 'unlikes']


class LikeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Like
        fields = ['url', 'who_liked', 'post', 'date']


class DislikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dislike
        fields = ['url', 'who_disliked', 'post', 'date']
