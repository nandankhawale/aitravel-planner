from django.urls import path
from .views import plan_trip,index,destinations,guides,testimonials,help

urlpatterns = [
    path("ask/", plan_trip, name="plan_trip"),
    path("index/", index, name="index"),
    path('destinations/',destinations, name='destinations'),
    path('guides/', guides, name='guides'),
    path('testimonials/',testimonials, name='testimonials'),
    path('help/', help, name='help')
  
]
