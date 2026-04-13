
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name= 'post_list'),
    path('profile/', views.profile, name='profile'),
    path('post/<int:id>',views.post_details, name= 'post_details'),
    path('post/<int:id>/like', views.liked_post, name= 'liked_post'),
    path('post/create', views.post_create, name= 'post_create'),
    path('post/update/<int:id>', views.post_update, name= 'post_update'),
    path('post/delete/<int:id>', views.post_delete, name= 'post_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
