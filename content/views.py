from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.shortcuts import render_to_response
from content.models import *


def page(request, slug):
    data = {
        'item': Page.objects.get(slug=slug, visibility=True),
    }
    return render_to_response('content/page.html', data)


class ArticlesList(ListView):
    model = Article
    paginate_by = 10
    template_name = 'articles/list.html'

    def get_queryset(self):
        objects = self.model.objects.filter(visibility=True)

        if self.kwargs.get('category'):
            objects = objects.filter(category__id=self.kwargs['category'])

        return objects

    def get_context_data(self, **kwargs):
        context = super(ArticlesList, self).get_context_data(**kwargs)

        context['menu'] = 'catalog'
        context['submenu'] = 'articles'
        context['categories'] = ArticleCategory.objects.all()

        return context


class ArticlePage(DetailView):
    model = Article
    context_object_name = 'item'
    template_name = 'articles/detail.html'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super(ArticlePage, self).get_context_data(**kwargs)
        context['menu'] = 'catalog'
        context['submenu'] = 'articles'

        context['other'] = self.model.objects.select_related().filter(visibility=True).exclude(pk=object.id)[0:5]
        #context['comments'] = Comment.objects.select_related().filter(entity='clinics', id_entities=object.id, visibility=True).order_by('-created')[0:3]

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
        
        return redirect('/clinics/%s?' % object.id)
