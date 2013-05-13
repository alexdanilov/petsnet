from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from nurseries.models import *
from content.models import Comment
from news.models import News
from system.models import Region


class NurseriesList(ListView):
    model = Nursery
    paginate_by = 10
    template_name = 'nurseries/list.html'

    def get_queryset(self):
        objects = self.model.objects.filter(visibility=True)

        if self.request.GET.get('q'):
            objects = objects.filter(name__icontains=self.request.GET.get('q'))
        if self.request.GET.get('region'):
            objects = objects.filter(region__region_id=int(self.request.GET['region']))
        if self.request.GET.getlist('type'):
            objects = objects.filter(type__in=self.request.GET.getlist('type'))
        if self.request.GET.getlist('service'):
            objects = objects.filter(services__id__in=self.request.GET.getlist('service'))

        if self.request.GET.get('sort') in ['begin_date', 'name']:
            objects = objects.order_by(self.request.GET.get('sort'))

        return objects

    def get_context_data(self, **kwargs):
        context = super(NurseriesList, self).get_context_data(**kwargs)

        context['menu'] = 'catalog'
        context['submenu'] = 'nurseries'
        context['all_services'] = NurseryService.objects.all()
        context['filter'] = {
            'order_by': self.request.GET.get('sort', ''),
            'city': self.request.GET.get('city', 0),
            'region': self.request.GET.get('region', 0),
            'type': self.request.GET.getlist('type')
        }

        context['regions'] = Region.objects.filter(country_id=2).values('region_id', 'region').distinct()
        if self.request.GET.get('region'):
            context['cities'] = Region.objects.filter(region_id=int(self.request.GET.get('region'))).order_by('city')
        if self.request.GET.getlist('service'):
            context['filter']['services'] = NurseryService.objects.filter(id__in=self.request.GET.getlist('service'))

        return context


class NurseryPage(DetailView):
    model = Nursery
    context_object_name = 'item'
    template_name = 'nurseries/detail.html'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super(NurseryPage, self).get_context_data(**kwargs)

        if self.request.method == 'POST':
            new_comment = Comment(**{
                'entity': 'nurseries',
                'id_entities': object.id,
                'user': request.member,
                'comment': request.POST['comment'],
                'visibility': True,
            })
            new_comment.save()
            return redirect(object.url)

        context['menu'] = 'catalog'
        context['submenu'] = 'nurseries'
        context['other'] = self.model.objects.select_related().filter(visibility=True).exclude(pk=object.id)[0:5]
        context['news'] = News.objects.select_related().filter(entity='nurseries', id_entities=object.id, visibility=True).order_by('-created')[0:3]
        context['comments'] = Comment.objects.select_related().filter(entity='nurseries', id_entities=object.id, visibility=True).order_by('-created')[0:3]

        return context

