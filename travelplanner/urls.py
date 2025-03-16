from django.urls import path
from .views import plan_trip,index

urlpatterns = [
    path("ask/", plan_trip, name="plan_trip"),
    path("index/", index, name="index"),
  
]
