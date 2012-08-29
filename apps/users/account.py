import datetime
import hashlib
import simplejson
import urllib, urllib2

from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from apps.users.models import UserProfile


LOGINZA_ID = 2851
LOGINZA_CODE = '5432e8b52f1bdf473fcf12152cf3d147'


@csrf_exempt
def loginza(request):
    token = request.POST.get('token')
    LOGINZA_SIG = hashlib.md5(token + LOGINZA_CODE).hexdigest()
    url = 'http://loginza.ru/api/authinfo?token=%s&id=%s&sig=%s' % (token, LOGINZA_ID, LOGINZA_SIG)
    data = simplejson.load(urllib2.urlopen(url))

    if data.has_key('email'):
        try:
            user = UserProfile.objects.get(email=data.get('email'))
        except UserProfile.DoesNotExist:
            user_data = {'balance': 0, 'balls': 0, 'activate': True, 'last_login': datetime.datetime.now()}
            try:
                user_data['first_name'], user_data['last_name'] = data['name']['full_name'].split(' ')

                year, day, month = data.get('dob').split('-')
                user_data['birth_day'] = '%s-%s-%s' % (year, month, day)

                user_data['email'] = data.get('email', '')
                user_data['gender'] = data.get('gender').lower()
            except Exception:
                pass
            user = UserProfile(**user_data)
        
        user.last_login = datetime.datetime.now()
        user.save()
        request.session['user'] = user.id
        response = redirect('/my/home/')
        response.set_cookie('user', user.id)
    else:
        response = redirect('/users/signin/?errors=%s' % urllib.urlencode(data))
    
    return response


def signin(request):
    data = {}
    data['host'] = request.META.get('HTTP_HOST')
    data['error'] = True if request.GET.has_key('errors') else False
    return render_to_response('users/signin.html', data)


def signout(request):
    del request.session['user']
    return redirect('/')


def signup(request):
    return render_to_response('users/signup.html', {})
