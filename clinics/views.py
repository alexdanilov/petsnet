from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import redirect

from clinics.models import *
from content.models import Comment
from news.models import News
from system.models import Region


class ClinicsList(ListView):
    model = Clinic
    paginate_by = 10
    template_name = 'clinics/list.html'

    def get_queryset(self):
        objects = self.model.objects.filter(visibility=True)

        if self.request.GET.get('q'):
            objects = objects.filter(name__icontains=self.request.GET.get('q'))
        if self.request.GET.get('region'):
            objects = objects.filter(region__region_id=int(self.request.GET['region']))
        #if self.request.GET.get('city'):
            #objects = objects.filter(region__city_id=int(self.request.GET['city']))
        if self.request.GET.getlist('service'):
            objects = objects.filter(services__id__in=self.request.GET.getlist('service'))

        if self.request.GET.get('sort') in ['rating', 'name']:
            objects = objects.order_by(self.request.GET.get('sort'))

        return objects

    def get_context_data(self, **kwargs):
        context = super(ClinicsList, self).get_context_data(**kwargs)

        context['menu'] = 'catalog'
        context['submenu'] = 'clinics'
        context['all_services'] = ClinicService.objects.all()
        context['filter'] = {
            'order_by': self.request.GET.get('sort', ''),
            'city': self.request.GET.get('city', 0),
            'region': self.request.GET.get('region', 0),
        }

        context['regions'] = Region.objects.filter(country_id=2).values('region_id', 'region').distinct()
        if self.request.GET.get('region'):
            context['cities'] = Region.objects.filter(region_id=int(self.request.GET.get('region'))).order_by('city')
        if self.request.GET.getlist('service'):
            context['filter']['services'] = ClinicService.objects.filter(id__in=self.request.GET.getlist('service'))


        return context


class ClinicPage(DetailView):
    model = Clinic
    context_object_name = 'item'
    template_name = 'clinics/detail.html'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super(ClinicPage, self).get_context_data(**kwargs)

        context['menu'] = 'catalog'
        context['submenu'] = 'clinics'
        context['other'] = self.model.objects.select_related().filter(visibility=True).exclude(pk=object.id)[0:5]
        context['news'] = News.objects.select_related().filter(entity='clinics', id_entities=object.id, visibility=True).order_by('-created')[0:3]
        context['comments'] = Comment.objects.select_related().filter(entity='clinics', id_entities=object.id, visibility=True).order_by('-created')[0:3]

        return context

    def post(self, request, *args, **kwargs):
        object = self.get_object()

        # save comment
        new_comment = Comment(
            entity = 'clinics',
            id_entities = object.id,
            user = request.member,
            comment = request.POST['comment'],
            visibility = True
        )
        new_comment.save()
        
        return redirect('/clinics/%s/?' % object.id)

