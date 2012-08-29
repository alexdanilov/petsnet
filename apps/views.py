import datetime

from django.views.generic import TemplateView
from django.template.loader import add_to_builtins

from apps.announcements.models import Announcement, TYPE_CHOICES as ANNOUNCEMENT_TYPES
from apps.clinics.models import Clinic
from apps.exhibitions.models import Exhibition
from apps.nurseries.models import Nursery
from apps.pharmacies.models import Pharmacy


# add extra tags to builtins
add_to_builtins('system.templatetags.extra_tags')


class IndexView(TemplateView):
    template_name = 'mainpage.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        now = datetime.datetime.now()

        # catalog items
        context['clinics'] = Clinic.objects.select_related().filter(visibility=True).order_by('?')[0:3]
        context['nurseries'] = Nursery.objects.select_related().filter(visibility=True).order_by('?')[0:3]
        context['pharmacies'] = Pharmacy.objects.select_related().filter(visibility=True).order_by('?')[0:3]

        # interesting items
        context['exhibitions'] = Exhibition.objects.select_related().filter(begin_date__lte=now, visibility=True).order_by('-begin_date')[0:5]

        # get announcements by type
        context['announcements_types'] = ANNOUNCEMENT_TYPES
        for key, name in ANNOUNCEMENT_TYPES:
            context['announcements_' + key.replace('-', '_')] = Announcement.objects.select_related().filter(type=key).order_by('-created')[0:3]
        
        return context




