import datetime
import hashlib
import urllib, urllib2

from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from apps.users.models import UserProfile



def signin(request):
    data = {}
    data['host'] = request.META.get('HTTP_HOST')
    data['error'] = True if request.GET.has_key('errors') else False
    return render_to_response('users/signin.html', data)


def signout(request):
    if request.session.has_key('user'):
        del request.session['user']
    return redirect('/')


def signup(request):
    return render_to_response('users/signup.html', {})
