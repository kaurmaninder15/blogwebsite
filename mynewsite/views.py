from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from .forms import PostBlog, CommentForm, UserSigninForm, UserRegistrationForm
from .models import Post, PostComments

# Create your views here.

class Signin(TemplateView):
    extra_context = {'form': UserSigninForm()}
    template_name = 'signin.html'

    def post(self, request):
        form = UserSigninForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                user = authenticate(username=request.POST['username'], password=request.POST['password'])

                if user is not None:
                    login(request, user)

                    return render(request, 'index.html')
                else:
                    return render(request, 'signin.html', context={'form': form, 'error': 'Invalid username or password'})
            except:
                pass

            return render(request, 'signin.html', context={'form': form})
        else:
            return render(request, 'signin.html', context={'form': form})

class Signup(TemplateView):
    extra_context = {'form': UserRegistrationForm()}
    template_name = 'signup.html'


    def post(self,request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            if request.POST['password'] != request.POST['confirm_password']:
                return render(request,'signup.html',context={'form':form,'error':'Password and confirm password does not match'})

            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request,'signup.html',context={'form':form,'error':'Username already exists'})
            except:
                pass

            try:
                user = User.objects.get(email=request.POST['email'])
                return render(request,'signup.html',context={'form':form,'error':'Email already exists'})
            except:
                pass

            user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'],password=request.POST['password'])
            user.save()

            return render(request,'signup.html',context={'form':form})
        else:
            return render(request,'signup.html',context={'form':form})


def Index(request):
    post_list = Post.objects.all().order_by('-id')
    context = {'post_list': post_list}
    return render(request,'index.html', context)

def Single(request,pk):
    form = CommentForm()
    post_comment = PostComments.objects.filter(post=pk)
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return HttpResponse('Post not found')
    return render(request, 'single.html', {'post': post, 'form': form, 'post_comment': post_comment})


def like_post(request,pk):
    if request.user.is_authenticated:
        post=Post.objects.get(id=pk)
        if request.user in post.like_by.all():
            pass
        else:
            post.like_by.add(request.user)
        return redirect('single',pk=pk)
    else:
        return HttpResponse('You need to login to like or dislike the post')


def dislike_post(request,pk):
    post=Post.objects.get(id=pk)
    if request.user in post.like_by.all():
        post.like_by.remove(request.user)
    else:
        pass
    return redirect('single',pk=pk)


def create_blog(request):
    form = PostBlog()
    if request.method == 'POST':
        form = PostBlog(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            active = form.cleaned_data['active']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            user = request.user.username
            # author=form.cleaned_data['author']
            # tags=form.cleaned_data['tags']
            status = form.cleaned_data['status']
            post = Post.objects.create(title=title, description=description, active=active, image=image, category_id=category,user=user,status=status)
            # post.tags.set(tags)

            post.save()
            return redirect('index')
            return HttpResponse('Blog created successfully')
        else:
            return render(request,'create_blog.html',{'form':form})
    else:
        if request.user.has_perm('blog.add_post'):
         # return render(request,'create_blog.html',{'form':form})
            return render(request, 'create_blog.html', {'form': PostBlog()})
        else:
            return HttpResponse('You are not allowed to create post')


def update_blog(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        form = PostBlog(
            initial={'title': post.title, 'description': post.description, 'active': post.active,
                     'image': post.image, 'category': post.category, 'status': post.status})


        if request.method == 'POST':
            form = PostBlog(initial={'title': post.title, 'description': post.description,
                                     'category': post.category,  'status': post.status,
                                     'active': post.active, 'image': post.image})

            # form = PostBlog(request.POST,request.FILES)
            if form.is_valid():
                post.title = form.cleaned_data['title']
                post.description = form.cleaned_data['description']
                post.category = form.cleaned_data['category']
                post.status = form.cleaned_data['status']
                post.save()

                return redirect('home')
        else:
            return render(request, 'update_blog.html', {'form': form, 'error': 'Invalid data'})

def delete_blog(request,pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return HttpResponse('Blog deleted successfully')

def post_comments(request,pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            post = Post.objects.get(id=pk)
            PostComments.objects.create(comment=comment, post=post)
            return redirect('single',pk=pk)


