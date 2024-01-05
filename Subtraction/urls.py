from django.urls import path
from .views import *

urlpatterns = [
    path('subtract_images/', SubtractImagesAPIView.as_view(), name='subtract_images'),
]