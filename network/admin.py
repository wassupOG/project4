from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    ordering = ('-date', )
    list_display = ('user', 'likes', 'date')

class FollowerAdmin(admin.ModelAdmin):
    ordering = ('-date', )
    list_display = ('follower', 'following', 'date')

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follower, FollowerAdmin)