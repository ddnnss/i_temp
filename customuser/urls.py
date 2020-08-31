from django.urls import path
from . import views

urlpatterns = [

   path('logout/', views.logout_page, name='logout_page'),
   path('register/', views.register, name='register'),
   path('login_req/', views.login_req, name='login_req'),
   path('profile/', views.profile_index, name='profile_index'),
   path('transfer/', views.transfer, name='transfer'),



]
