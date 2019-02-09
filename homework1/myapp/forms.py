from django.contrib.auth.models import User
from django.contrib.contenttypes import forms
from django.forms import Form, ModelForm, BaseInlineFormSet

from myapp.models import UserProfile, Post


class ProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileImage(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'profile_image']


class NewPost(ModelForm):
    class Meta:
        model = Post
        fields = ['user', 'img']


""" 
def __init__(self, **kwargs):
     self.user = kwargs.pop('user', None)
     self.img = kwargs.pop('img', None)
     super(NewPost, self).__init__(**kwargs)
 def save(self, commit=True):
     obj = super(NewPost, self).save(commit=False)
     obj.user = self.user
     obj.img = self.img
     if commit:
         obj.save()
     return obj
 """
