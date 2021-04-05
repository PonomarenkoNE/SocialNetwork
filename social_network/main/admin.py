from django.contrib import admin
from .models import Post, Like, Dislike

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Dislike)
