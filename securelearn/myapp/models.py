from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

#This is ths model for the tutorial
class tutorial(models.Model):
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True) #slug is a field meant to be used in URLs. A slug field in Django is used to store and generate valid URLs for your dynamically created web pages. A slug field in Django is created using the SlugField class. A slug field in Django is a field used to store and generate valid URLs for your dynamically created web pages.
    description = models.TextField()
    content = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True, editable=False)
    updated_at= models.DateTimeField(auto_now=True, editable=False)
    image = models.ImageField(upload_to='tutorialimages/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    '''
    This method will generate the absolute URL for a Tutorial instance,
        facilitating easy redirection and linking. It utilizes the reverse function
        to build the URL based on the 'post_single' URL pattern and the Tutorial's slug.
    '''

    def get_absolute_url(self):
        return reverse("post_single", args=[self.slug])
    
    def update_average_rating(self):
        ratings = ratetutorial.objects.filter(tutorial=self)
        total_ratings = ratings.count()
        if total_ratings > 0:
            average_rating = sum([rating.rating for rating in ratings]) / total_ratings
            self.average_rating = round(average_rating, 2)
        else:
            self.average_rating = 0.0
        self.save()


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

#This is the model for the rating system  
class ratetutorial(models.Model):
    tutorial = models.ForeignKey('tutorial', related_name='ratetutorials', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    class Meta:
        unique_together = ('tutorial', 'user')

    def __str__(self):
        return '%s rated %s' % (self.user.username, self.tutorial.title)

#This is the model for the admin (which will be added to the admin group by the superuser from django admin dashboard)
class AppAdmin(models.Model):
   
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=True)
   

    def __str__(self):
        return self.username
    

    

class registeredusers(models.Model):
    
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
   

    def __str__(self):
        return self.username
    



class comment(models.Model):
    name = models.CharField(max_length=255)
    post = models.ForeignKey('tutorial', related_name='comments' ,on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
    

class joke(models.Model):
    joke = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.joke
    
    


    
