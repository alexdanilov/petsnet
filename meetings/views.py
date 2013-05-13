import urllib
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from apps.exhibitions.models import *
from apps.content.models import Comment


class ExhibitionsList(ListView):
    model = Exhibition
    paginate_by = 10
    template_name = 'exhibitions/list.html'

    def get_queryset(self):
        objects = self.model.objects.filter(visibility=True)

        if self.request.GET.get('q'):
            objects = objects.filter(name__icontains=self.request.GET.get('q'))

        if self.request.GET.get('sort') in ['rating', 'name']:
            objects = objects.order_by(self.request.GET.get('sort'))

        return objects

    def get_context_data(self, **kwargs):
        context = super(ClinicsList, self).get_context_data(**kwargs)

        context['menu'] = 'events'
        context['submenu'] = 'exhibitions'
        context['filter'] = {'order_by': self.request.GET.get('sort', '')}

        items = self.model.objects.filter(visibility=True)
        context['regions'] = items.values('region__region').distinct()

        return context


class ExhibitionPage(DetailView, ClinicsContext):
    model = Exhibition
    context_object_name = 'item'
    template_name = 'exhibitions/detail.html'

    def get_context_data(self, **kwargs):

        if request.method == 'POST':
            new_comment = Comment(**{
                'entity': 'exhibitions',
                'id_entities': data['item'].id,
                'user': request.member,
                'comment': request.POST['comment'],
                'visibility': True,
            })
            new_comment.save()
            return redirect('/clinics/show/%s' % id)

        data['url'] = urllib.urlencode(data['filter'])
        data['other'] = Clinic.objects.select_related().filter(visibility=True).exclude(pk=data['item'].id)[0:5]
        data['news'] = CatalogNews.objects.select_related().filter(entity='clinics', id_entities=data['item'].id, visibility=True).order_by('-created')[0:3]
        data['comments'] = Comment.objects.select_related().filter(entity='clinics', id_entities=data['item'].id, visibility=True).order_by('-created')[0:3]

