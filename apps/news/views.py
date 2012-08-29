from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from apps.news.models import CatalogNews
from apps.content.models import Comment


class CatalogNewsList(ListView):
    model = CatalogNews
    paginate_by = 10
    template_name = 'news/list.html'

    def get_queryset(self):
        objects = self.model.objects.filter(visibility=True)

        if self.request.GET.get('q'):
            objects = objects.filter(name__icontains=self.request.GET.get('q'))

        if self.request.GET.get('sort') in ['rating', 'name']:
            objects = objects.order_by(self.request.GET.get('sort'))

        return objects

    def get_context_data(self, **kwargs):
        context = super(CatalogNewsList, self).get_context_data(**kwargs)

        context['menu'] = 'events'
        context['submenu'] = 'news'
        context['filter'] = {'order_by': self.request.GET.get('sort', '')}

        return context


class CatalogNewsPage(DetailView):
    model = CatalogNews
    context_object_name = 'item'
    template_name = 'news/detail.html'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super(CatalogNewsPage, self).get_context_data(**kwargs)

        if self.request.method == 'POST':
            new_comment = Comment(**{
                'entity': 'news',
                'id_entities': object.id,
                'user': self.request.member,
                'comment': self.request.POST['comment'],
                'visibility': True,
            })
            new_comment.save()
            return redirect(object.url)

        context['other'] = self.model.objects.select_related().filter(visibility=True).exclude(pk=object.id)[0:5]
        context['comments'] = Comment.objects.select_related().filter(entity='clinics', id_entities= object.id, visibility=True).order_by('-created')[0:3]

        return context

