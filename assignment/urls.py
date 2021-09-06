from django.contrib import admin
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from .views import ValidationApi
urlpatterns = [
    path('api/', csrf_exempt(ValidationApi.as_view()))
    ,
]
