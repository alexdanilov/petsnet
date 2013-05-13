from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from exhibitions.models import *
from content.models import Comment
from news.models import News
from system.models import Region


class ExhibitionsList(ListView):
    model = Exhibition
    paginate_by = 10
    template_name = 'exhibitions/list.html'

    def get_queryset(self):
        objects = self.model.objects.filter(visibility=True)

        if self.request.GET.get('q'):
            objects = objects.filter(name__icontains=self.request.GET.get('q'))
        if self.request.GET.getlist('type'):
            objects = objects.filter(type__in=self.request.GET.getlist('type'))

        if self.request.GET.get('sort') in ['begin_date', 'name']:
            objects = objects.order_by(self.request.GET.get('sort'))

        return objects

    def get_context_data(self, **kwargs):
        context = super(ExhibitionsList, self).get_context_data(**kwargs)

        context['menu'] = 'events'
        context['submenu'] = 'exhibitions'
        context['filter'] = {
            'order_by': self.request.GET.get('sort', ''),
            'city': self.request.GET.get('city', 0),
            'region': self.request.GET.get('region', 0),
            'type': self.request.GET.getlist('type')
        }

        context['regions'] = Region.objects.filter(country_id=2).values('region_id', 'region').distinct()
        if self.request.GET.get('region'):
            context['cities'] = Region.objects.filter(region_id=int(self.request.GET.get('region'))).order_by('city')

        return context


class ExhibitionPage(DetailView):
    model = Exhibition
    context_object_name = 'item'
    template_name = 'exhibitions/detail.html'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super(ExhibitionPage, self).get_context_data(**kwargs)

        if self.request.method == 'POST':
            new_comment = Comment(**{
                'entity': 'exhibitions',
                'id_entities': object.id,
                'user': self.request.member,
                'comment': self.request.POST['comment'],
                'visibility': True,
            })
            new_comment.save()
            return redirect('/exhibitions/%s' % id)

        context['menu'] = 'events'
        context['submenu'] = 'exhibitions'
        context['other'] = self.model.objects.select_related().filter(visibility=True).exclude(pk=object.id)[0:5]
        context['news'] = News.objects.select_related().filter(entity='exhibition', id_entities=object.id, visibility=True).order_by('-created')[0:3]
        context['comments'] = Comment.objects.select_related().filter(entity='exhibition', id_entities=object.id, visibility=True).order_by('-created')[0:3]

        return context

