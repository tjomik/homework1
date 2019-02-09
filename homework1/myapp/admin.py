from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from myapp.models import Post, Like, Follower, Comment, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    search_fields = ['first_name']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)
admin.site.register(Comment)