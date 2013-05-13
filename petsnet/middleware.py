from django.conf import settings
from users.models import UserProfile


SITES = {
    'petsnet.in.ua': 1,
    'petsnet.ru': 2,
    'petsnet.kz': 3,
    'petsnet.by': 4,
}


class PetsnetMiddleware(object):
    
    def process_request(self, request):
        host = request.META.get('HTTP_HOST', '')
        request.__class__.site_id = SITES.get(host.replace('www.', ''), 1)
        
        if settings.DEBUG:
            #request.session['user'] = 1
            pass
        if request.session.get('user'):
            request.__class__.member = UserProfile.objects.get(pk=request.session['user'])
        else:
            request.__class__.member = {}
