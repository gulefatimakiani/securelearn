from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from .models import *
from .forms import CreateUserForm, tutorial_form, RatingForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import comment_form
import datetime
from .decorators import allowed_users
from django.http import JsonResponse
from django.views.decorators.http import require_POST




# Create your views here.

# This is the view for the home page
def HomeView(request):
    tutorials = tutorial.objects.all().order_by('-created_at')[:3]
    jokes = joke.objects.all().order_by('-created_at')[:4]
    context = {'tutorials': tutorials, 'jokes': jokes}
    return render(request, 'index.html', context)

# This is the view for the page where all tutorials are displayed
def TutorialsView(request):
    tutorials = tutorial.objects.all()
    return render(request, 'alltutorials.html', {'tutorials': tutorials})


# This is the view for the page where a single tutorial is displayed
def post_single(request, post):
    post = get_object_or_404(tutorial, slug=post)
    number_of_comments = comment.objects.filter(post=post).count()
    related = tutorial.objects.filter(author= post.author)[:4]
    rating_form = RatingForm(initial={'tutorial_id': post.id})
    user_rating = 0
    if request.user.is_authenticated:
        user_rating_obj = ratetutorial.objects.filter(user=request.user, tutorial=post).first()
        if user_rating_obj:
            user_rating = user_rating_obj.rating

    context = {'post': post, 
            'number_of_comments': number_of_comments,
            'related': related,
            'user_rating': user_rating,
            'rating_form': rating_form}
    
    return render(request, "tutorialdetail.html", context)


# This is the view for the page where a user can register
def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method != 'POST':
            form = CreateUserForm()
        else:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('login')

        context = {'form': form}

        return render(request, 'register.html', context)

# This is the view for the page where a user can login
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate (request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, "Username or Password is incorrect")
                return render(request, "login.html")
        context = {}
        return render(request, "login.html", context)

def logoutuser(request):
    logout(request)
    return redirect('/')

# This is the view for the page where a user can add a comment: @login_required decorator is used to ensure that only logged in users can add comments
@login_required(login_url='login')
def add_comment(request, post):
    post = get_object_or_404(tutorial, slug=post)
    form = comment_form(instance=post)
    if request.method == 'POST':
        form = comment_form(request.POST, instance=post)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['body']

            c = comment(name=name, post=post, body=body, created_at=datetime.datetime.now())
            c.save()
        return redirect('post_single', post=post.slug)
    else:
        form=comment_form(instance=post)

    context = {'form': form}

    return render(request, 'base/add_comment.html', context)

# This is the view for the page where a user can delete a comment: @login_required decorator is used to ensure that only logged in users can delete comments
@login_required(login_url='login')
def delete_comment(request, post, pk):
    post = get_object_or_404(tutorial, slug=post)
    c = comment.objects.get(pk=pk)
    c.delete()
    return redirect('post_single', post=post.slug)


# This is the view for the page where an admin can add/update/delete tutorials. @login_required decorator is used to ensure that only logged in admin can manage tutorials
# @allowed_users decorator is used to ensure that only admin can view this page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def manage_posts(request):
   user=request.user
   post = tutorial.objects.filter(author=user)
   posts_count= tutorial.objects.all().count()
   users = User.objects.all().count()
   context = {'post':post,'posts_count': posts_count, 'users': users}
   return render(request, 'manage_posts.html', context)

# This is the view for the page where an admin can create a new tutorial
def create_tutorial(request):
    if request.method != 'POST':
        form = tutorial_form()
    else:
        form = tutorial_form(request.POST, request.FILES)
        if form.is_valid():
            author = request.user.username
            form.save()
            return redirect('manage_posts')
    context = {'form': form}
    return render(request, 'create_tutorial.html', context)

# This is the view for the page where an admin can update a tutorial
def update_tutorial(request, post):
    post = get_object_or_404(tutorial, slug=post)
    if request.method != 'POST':
        form = tutorial_form(instance=post)
    else:
        form = tutorial_form(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('manage_posts')
    context = {'form': form}
    return render(request, 'create_tutorial.html', context)

# This is the view for the page where an admin can delete a tutorial
def delete_tutorial(request, post): 
    post = get_object_or_404(tutorial, slug=post)
    if request.method == 'POST':
        post.delete()
        return redirect('manage_posts')
    context = {'post': post}
    return render(request, 'delete_tutorial.html', context)

# This is the view for the page where a user can view the about us information
def aboutus(request):
    return render(request, 'about_us.html')

# This is the view for the page where a user can view the jokes
def joke_carousel(request):
    jokes = joke.objects.all()
    return render(request, 'index.html', {'jokes': jokes})
   

def add_comment(request, post):
    post = get_object_or_404(tutorial, slug=post)
    form = comment_form(instance=post)
    if request.method == 'POST':
        form = comment_form(request.POST, instance=post)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['body']

            c = comment(name=name, post=post, body=body, created_at=datetime.datetime.now())
            c.save()
        return redirect('post_single', post=post.slug)
    else:
        form=comment_form(instance=post)

    context = {'form': form}

    return render(request, 'base/add_comment.html', context)

'''
def delete_comment(request, post, created_at):
    post = get_object_or_404(tutorial, slug=post)
    c = comment.objects.get(created_at=created_at)
    if request.user == c.name:
        c.delete()
        return redirect('post_single', post=post.slug)
    else:
        # Handle unauthorized deletion attempt
        return render(request, 'unauthorized_delete.html')

'''
'''
@login_required(login_url='login')
def rating(request, post):
    post = get_object_or_404(tutorial, slug=post)
    if request.method == 'POST':
        try:
            rating = ratetutorial.objects.get(user__id=request.user.id, tutorial__slug=post.slug)
            form = rating_form(request.POST, instance=rating)
            form.save()
            messages.success(request, "Thank you for rating this tutorial")
            return redirect('tutorial_detail.html', post=post.slug)
        except ratetutorial.DoesNotExist:
            form = rating_form(request.POST)
            if form.is_valid():
                data = ratetutorial()
                data.user = request.user
                data.tutorial = post
                data.score = form.cleaned_data['rating']
                data.save()
                messages.success(request, "Thank you for rating this tutorial")
                return redirect('tutorial_detail.html', post=post.slug) -->
   '''             
        
@require_POST
@login_required
def rate_tutorial(request):
    form = RatingForm(request.POST)

    if form.is_valid():
        rating = form.cleaned_data['rating']
        tutorial_slug = form.cleaned_data['tutorial_slug']

        # Use get_object_or_404 to retrieve the tutorial object using slug
        tutorial_obj = get_object_or_404(tutorial, slug=tutorial_slug)

        user_rating_obj, created = ratetutorial.objects.get_or_create(user=request.user, tutorial=tutorial_obj)
        user_rating_obj.rating = rating
        user_rating_obj.save()

        # Update the average rating for the tutorial
        tutorial_obj.update_average_rating()

        messages.success(request, 'Rating submitted successfully!')
    else:
        messages.error(request, 'Failed to submit rating. Please check the form.')

    # Redirect back to the tutorial detail page
    return redirect('post_single', post=tutorial_obj.slug)




       







