from django.contrib import admin
from django.urls import path, include
from .views import HomePageView, AuthorizeView, Oauth2CallbackView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', HomePageView.as_view(),  name='home'),
    path('authorize/', AuthorizeView.as_view(), name='authorize'),
    path('oauth2callback/', Oauth2CallbackView.as_view(), name='oauth2callback'),

]

