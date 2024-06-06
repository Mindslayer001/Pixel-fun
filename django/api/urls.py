from django.urls import path
from . import views
urlpatterns = [
 path("story/<str:option>/", views.story, name="story"),
]
