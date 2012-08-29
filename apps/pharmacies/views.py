from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from apps.pharmacies.models import *
from apps.content.models import Comment
from apps.news.models import CatalogNews


class PharmaciesList(ListView):
    model = Pharmacy
    paginate_by = 10
    template_name = 'pharmacies/list.html'

    def get_queryset(self):
        objects = self.model.objects.filter(visibility=True)

        if self.request.GET.get('q'):
            objects = objects.filter(name__icontains=self.request.GET.get('q'))

        if self.request.GET.get('sort') in ['rating', 'name']:
            objects = objects.order_by(self.request.GET.get('sort'))

        return objects

    def get_context_data(self, **kwargs):
        context = super(PharmaciesList, self).get_context_data(**kwargs)

        context['menu'] = 'catalog'
        context['submenu'] = 'pharmacies'
        context['filter'] = {'order_by': self.request.GET.get('sort', '')}

        items = self.model.objects.filter(visibility=True)
        context['regions'] = items.values('region__region').distinct()

        return context


class PharmacyPage(DetailView):
    model = Pharmacy
    context_object_name = 'item'
    template_name = 'pharmacies/detail.html'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super(PharmacyPage, self).get_context_data(**kwargs)

        if self.request.method == 'POST':
            new_comment = Comment(**{
                'entity': 'pharmacies',
                'id_entities': object.id,
                'user': request.member,
                'comment': request.POST['comment'],
                'visibility': True,
            })
            new_comment.save()
            return redirect(object.url)

        context['other'] = self.model.objects.select_related().filter(visibility=True).exclude(pk=object.id)[0:5]
        context['news'] = CatalogNews.objects.select_related().filter(entity='pharmacies', id_entities=object.id, visibility=True).order_by('-created')[0:3]
        context['comments'] = Comment.objects.select_related().filter(entity='pharmacies', id_entities=object.id, visibility=True).order_by('-created')[0:3]

        return context

