import json

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView, UpdateView, CreateView
from django_ajax.decorators import ajax

from myapp.forms import ProfileForm, ProfileImage, NewPost
from myapp.models import Post, Follower, Comment, UserProfile, Like


def main(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/feed/')
    else:
        return HttpResponseRedirect('/login/')


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/feed/')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return HttpResponseRedirect('/feed/')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


class Registration(FormView):
    template_name = 'registration.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
        login(self.request, new_user)
        return HttpResponseRedirect('/feed/')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/feed/')
        return super(Registration, self).get(request, *args, **kwargs)


class FeedView(ListView):
    template_name = 'feed.html'
    model = Post

    def get_queryset(self):
        user_ids = Follower.objects.values_list('user_2_id', flat=True).filter(user_1_id=self.request.user.id)
        user_ids_list = list(user_ids)
        user_ids_list.append(self.request.user.id)
        comments = Comment.objects.all()
        posts = Post.objects.filter(user_id__in=user_ids_list).order_by('Date').reverse()
        result_list = list(chain(posts, comments))
        return result_list

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = serializers.serialize("json", queryset)
        return JsonResponse(data, status=200, safe=False)


class CommentView(ListView):
        template_name = 'feed.html'
        model = Comment
        queryset = Comment.objects.all()


class ProfileView(UpdateView):

    template_name = 'profile.html'
    success_url = '../profile'
    fields = ['user', 'profile_image']

    def get_object(self, queryset=None):
        a = list(UserProfile.objects.filter(user=self.request.user))
        b = a[0]
        return b
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/profile')


def profile_view(request):
    if request.method == 'GET':
        a = list(UserProfile.objects.values_list('profile_image', flat=True).filter(user=request.user))
        try:
            b = a[0]
        except:
            b = []

        form1 = ProfileForm(initial={'username': request.user.username,
                                     'first_name': request.user.first_name,
                                     'last_name': request.user.last_name,
                                     'email': request.user.email})
        form2 = ProfileImage()

        return render(request, 'profile.html', {'form1': form1,
                                                'form2': form2['profile_image'],
                                                'current_image': b})
    else:
        form1 = ProfileForm(request.POST, instance=request.user)
        user = request.user
        user_values = request.POST.copy()
        user_values['user'] = user.id
        try:
            user_user = UserProfile.objects.get(user_id=request.user.id)
            form2 = ProfileImage(user_values, request.FILES, instance=user_user)
        except:
            form2 = ProfileImage(user_values, request.FILES)

        form1.save()
        form2.save()
        return redirect('http://127.0.0.1/profile/')

class NewPostView(FormView):

    form_class = NewPost
    template_name = 'NewPost1.html'
    success_url = '../feed/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return HttpResponseRedirect('/feed/')


def new_post_view(request):
    #image = request.FILES.get('img', False)
    #fs = FileSystemStorage(location="./posts")
    #filename = fs.save(image.name, image)
    #file_url = "/posts/"+image.name
    #Post.objects.create(img=image, user=request.user)
    if request.method == 'POST':
        #mutable = request.POST._mutable
        #request.POST._mutable = True
        #request.POST['user'] = request.user
        #request.POST._mutable = mutable
        user = request.user
        post_values = request.POST.copy()
        post_values['user'] = user.id
        form = NewPost(post_values, request.FILES)

        #form.user = request.user
        #form.img = request.FILES.get('img', False)
        form.save()
        return HttpResponse("OK")
    else:
        form = NewPost(initial={})


def AccProfView(request,  username):
    return render(request, 'account_profile.html', {'username': username})





def accProfView(request, username):
    a = list(User.objects.filter(username=username))
    b = a[0]
    posts = serializers.serialize('json', Post.objects.filter(user=b).order_by('Date').reverse())
    return JsonResponse(posts, safe=False)


def Feed_view(request):
    return render(request, 'feed1.html')


def feed_view(request):
    user_ids = Follower.objects.values_list('user_2_id', flat=True).filter(user_1_id=request.user.id)
    user_ids_list = list(user_ids)
    user_ids_list.append(request.user.id)
    post_list = Post.objects.filter(user_id__in=user_ids_list).order_by('Date').reverse()
    #comments = Comment.objects.filter(post__in=posts)
    #posts = serializers.serialize('json', Post.objects.filter(user_id__in=user_ids_list).order_by('Date').reverse())

    page = request.GET.get('page', request.GET['page'])
    paginator = Paginator(post_list, 3)


    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(request.POST['page'])
    except EmptyPage:
        posts = []
    post_serial = serializers.serialize('json', posts)
    return JsonResponse(post_serial, safe=False)


def like_view(request, post_id):

    if request.method == 'GET':
        a = list(Like.objects.filter(user=request.user, post_id=post_id))

        try:
            b = a[0]
        except:
            return HttpResponse("lol")
        like_serial = serializers.serialize('json', a)
        return JsonResponse(like_serial, safe=False)

    else:
        if Like.objects.filter(user=request.user, post_id=post_id).exists():
            Like.objects.filter(user=request.user, post_id=post_id).delete()
        else:
            Like.objects.create(post_id=post_id, user=request.user)

        #a = list(Like.objects.filter(user=request.user, post_id=post_id))

        #try:
         #   b = a[0]
        #except:
        #    Like.objects.create(post_id=post_id, user=request.user)
        #Like.objects.filter(user=request.user, post_id=post_id).delete()
        return HttpResponse("OK")


def who_liked_view(request, post_id):
    #likes_list = Like.objects.values('user_id').filter(post_id=post_id)
    #likes_serial = serializers.serialize('json', likes_list)
    #return JsonResponse(likes_serial, safe=False)

    likes_list = list()
    user_list = list(User.objects.values('username').filter(id__in=Like.objects.values('user_id').filter(post_id=post_id)))
    #like_serial = serializers.serialize('json', user_list)
    return JsonResponse(json.dumps(user_list), safe=False)


def follow_view(request, username):
    user_id = list(User.objects.values_list('id', flat=True).filter(username=username))[0]
    if request.method == 'GET':
        return JsonResponse(Follower.objects.filter(user_1_id=request.user.id, user_2_id=user_id).exists(), safe=False)
    else:
        if Follower.objects.filter(user_1_id=request.user.id, user_2_id=user_id).exists():
            Follower.objects.filter(user_1_id=request.user.id, user_2_id=user_id).delete()

        else:
            Follower.objects.create(user_1_id=request.user.id, user_2_id=user_id)
        return HttpResponse('OK')


def get_username(request, user_id):
    if request.method == 'GET':
        return HttpResponse(User.objects.values_list('username', flat=True).filter(id=user_id)[0])
