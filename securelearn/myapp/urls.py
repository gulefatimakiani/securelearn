from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
   
    path('admin/', admin.site.urls),
    path('manage_posts/', views.manage_posts, name='manage_posts'),
    path('manage_posts/create_tutorial/', views.create_tutorial, name='create_tutorial'),
    path('manage_posts/update_tutorial/<slug:post>', views.update_tutorial, name='update_tutorial'),
    path('manage_posts/delete_tutorial/<slug:post>', views.delete_tutorial, name='delete_tutorial'),
    path('rate_tutorial/', views.rate_tutorial, name='rate_tutorial'),
    path('register/', views.register_page, name='register'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('', views.HomeView, name='homepage'),
    path('tutorials/', views.TutorialsView, name='tutorialspage'),
   
    path('<slug:post>/', views.post_single, name='post_single'),
    path('<slug:post>/add_comment/', views.add_comment, name='add_comment'),
   # path('<slug:post>/<create_at:comment.created_at/delete/', views.delete_comment, name='delete_comment'),
    
   
    
    
    
    

    
]