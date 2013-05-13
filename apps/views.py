import datetime

from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.template.loader import add_to_builtins
from django.contrib.admin.models import LogEntry

from apps.announcements.models import Announcement, TYPE_CHOICES as ANNOUNCEMENT_TYPES
from apps.clinics.models import Clinic
from apps.content.models import Article, Page
from apps.exhibitions.models import Exhibition
from apps.nurseries.models import Nursery
from apps.pharmacies.models import Pharmacy
from apps.photoalbums.models import Photo



# add extra tags to builtins
add_to_builtins('apps.system.templatetags.extra_tags')


class IndexView(TemplateView):
    template_name = 'mainpage.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        now = datetime.datetime.now()

        context['day_photo'] = Photo.objects.filter(is_top=True).order_by('?')
        if len(context['day_photo']) > 0:
            context['day_photo'] = context['day_photo'][0]

        # catalog items
        context['clinics'] = Clinic.objects.select_related().filter(visibility=True).order_by('?')[0:3]
        context['nurseries'] = Nursery.objects.select_related().filter(visibility=True).order_by('?')[0:3]
        context['pharmacies'] = Pharmacy.objects.select_related().filter(visibility=True).order_by('?')[0:3]

        # interesting items
        context['exhibitions'] = Exhibition.objects.select_related().filter(begin_date__lte=now, visibility=True).order_by('-begin_date')[0:5]
        context['meetings'] = []
        context['articles'] = Article.objects.filter(visibility=True)[0:5]
        context['news'] = []

        # get announcements by type
        context['announcements_types'] = ANNOUNCEMENT_TYPES
        for key, name in ANNOUNCEMENT_TYPES:
            context['announcements_' + key.replace('-', '_')] = Announcement.objects.select_related().filter(type=key).order_by('-created')[0:3]
        
        return context


class PageView(DetailView):
    model = Page
    template_name = 'page.html'
    context_object_name = 'item'

    def get_object(self):
        return self.model.objects.get(slug=self.kwargs['slug'])


class LogsList(ListView):
    model = LogEntry
    paginate_by = 100
    template_name = 'logs/list.html'
    context_object_name = 'items'

    def get_queryset(self):
        skip = int(self.request.GET.get('skip', 0))
        limit = int(self.request.GET.get('limit', 500))
        return self.model.objects.all().order_by('-action_time')[skip:limit]
