"""homework1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from homework1 import settings
from myapp.views import Registration, main, logout_view, login_view, ProfileView, \
    NewPostView, AccProfView, accProfView, FeedView, feed_view, Feed_view, like_view, new_post_view, who_liked_view, \
    profile_view, follow_view, get_username

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', Registration.as_view()),
    path('', main),
    path('logout/', logout_view),
    path('api/feed/', feed_view),
    path('login/', login_view),
    path('profile/', profile_view),
    path('newpost/', new_post_view),
    path('api/account/<username>/', accProfView),
    path('account/<username>/', AccProfView),
    path('feed/', Feed_view),
    path('like/<post_id>', like_view),
    path('new/', NewPostView.as_view()),
    path('wholiked/<post_id>', who_liked_view),
    path('follow/<username>', follow_view),
    path('getusername/<user_id>', get_username),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
