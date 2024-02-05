from django.urls import path
from .views import submit_email, success

urlpatterns = [
    path('', submit_email, name='submit_email'),
    path('success/', success, name='success'),
]
