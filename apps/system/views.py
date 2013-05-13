from django.http import HttpResponse
#from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _

from apps.system.models import Region


def ajax_get_cities(request):
    objects = Region.objects.filter(region_id=int(request.GET.get('r', 0)))
    output = "\n".join(["<option value='%s'>%s</option>" % (o.id, o.city) for o in objects])
    return HttpResponse(output)


def search_cities(request):
    objects = Region.objects.filter(city__istartswith=request.GET.get('q', ''))
    output = "\n".join(["%s|%s" % (o.id, o.city) for o in objects])
    return HttpResponse(output)


def get_monthes(r=False):
    prefix = 'monthes-r' if r else 'monthes'
    monthes = [
        _('monthes-01'),
        _('monthes-02'),
        _('monthes-03'),
        _('monthes-04'),
        _('monthes-05'),
        _('monthes-06'),
        _('monthes-07'),
        _('monthes-08'),
        _('monthes-09'),
        _('monthes-10'),
        _('monthes-11'),
        _('monthes-12'),
    ]
    monthes = [
        _('monthes-r-01'),
        _('monthes-r-02'),
        _('monthes-r-03'),
        _('monthes-r-04'),
        _('monthes-r-05'),
        _('monthes-r-06'),
        _('monthes-r-07'),
        _('monthes-r-08'),
        _('monthes-r-09'),
        _('monthes-r-10'),
        _('monthes-r-11'),
        _('monthes-r-12'),
    ]
    #monthes = [(m, _('%s-%s' % (prefix, m))) for m in range(1, 13)]
    return monthes
