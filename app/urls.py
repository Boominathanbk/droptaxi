from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
   path('',views.homepage,name='homepage'),
   path('round',views.round, name='round'),
   path('booking',views.booking,name='booking'),
   path('round_booking',views.round_booking, name='round_booking'),
   
   path('enqurie/', views.enqurie, name='enqurie'), 
   path('enquries/', views.enquries, name='enquries'),
   path('terms', views.terms, name='terms'),
]

