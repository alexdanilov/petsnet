from django.db.models import Q
from django.http import HttpResponse
from apps.users.models import UserProfile



def ajax_get_users(request):
    q = request.GET.get('q', '')
    objects = UserProfile.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
    output = "\n".join(['%s|%s' % (o.id, o.name) for o in objects])
    return HttpResponse(output)
