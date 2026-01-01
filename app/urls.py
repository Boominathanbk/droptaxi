from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('round',views.round, name='round'),
    path('booking',views.booking, name='booking'),
    path('enquries/', views.enquries, name='enquries'),
    path('login',views.login,name='login'),
    path('login_data',views.login_data,name='login_data'),
    path('round_booking',views.round_booking, name='round_booking'),
    path('roundtrip',views.roundtrip, name='roundtrip'),
    path('about',views.about, name='about'),

]