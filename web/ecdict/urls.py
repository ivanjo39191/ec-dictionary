from django.urls import path
from django.urls.conf import include

from . import views

urlpatterns = [
    path('form/', views.ECDictFormView.as_view(), name='ecdict_form'),
]