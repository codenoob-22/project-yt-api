from django.shortcuts import render
import requests

# Create your views here.

def index(request):
    url = 'https://googleapis.com/youtube/v3/'