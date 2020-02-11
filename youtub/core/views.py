from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django import forms

from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib import xsrfutil

from .models import CredentialsModel
# Create your views here.


class YouTubeForm(forms.Form):
    pass

class HomePageView(TemplateView):
    template_name = 'core/home.html'
    form_class = YouTubeForm

flow = OAuth2WebServerFlow(
    client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    scope = 'https://www.googleapis.com/auth/youtube',
    redirect_uri='https://localhost:8000/oauth2callback/'
)

class AuthorizeView(View):

    def get(self, request, *args, **kwargs):
        storage = DjangoORMStorage(
            CredentialsModel,
            'id',
            request.user.id,
            'credential'
        )
        credential = storage.get()

        flow = OAuth2WebServerFlow(
            client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
            client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            scope = 'https://www.googleapis.com/auth/youtube',
            redirect_uri='https://localhost:8000/oauth2callback/'
        )
        if credential is None or credential.invalid == True:
            flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
            authorize_url = flow.step1_get_authorize_url()
            return redirect(authorize_url)
        
        return redirect('/')

class Oauth2CallbackView(View):
    def get(self, request, *args, **kwargs):
        if not xsrfutil.validate_token(
            settings.SECRET_KEY,
            request.GET.get('state').encode(),
            request.user):
            return HttpResponseBadRequest()

        credential = flow.step2_exchange(request.GET)
        storage = DjangoORMStorage(
            CredentialsModel,
            'id',
            request.user.id,
            'credential'
        )
        storage.put(credential)
        return redirect('/')


