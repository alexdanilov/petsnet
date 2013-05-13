from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import redirect

from apps.animals.models import AnimalType
from apps.questions.models import *
from apps.users.generic import UserListView, UserCreateView, UserUpdateView, UserDeleteView



class QuestionsList(ListView):
    model = Question
    paginate_by = 10
    template_name = 'questions/list.html'

    def get_queryset(self):
        objects = self.model.objects.all()

        if self.request.GET.get('q'):
            objects = objects.filter(name__icontains=self.request.GET.get('q'))
        if self.request.GET.get('type'):
            objects = objects.filter(animal_type__id=self.request.GET.get('type'))
        if self.request.GET.get('category'):
            objects = objects.filter(category__id=self.request.GET.get('category'))

        if self.request.GET.get('sort') in ['begin_date', 'name']:
            objects = objects.order_by(self.request.GET.get('sort'))

        return objects

    def get_context_data(self, **kwargs):
        context = super(QuestionsList, self).get_context_data(**kwargs)

        context['menu'] = 'catalog'
        context['submenu'] = 'questions'
        context['types'] = AnimalType.objects.all()
        context['categories'] = Category.objects.all().order_by('order_num')
        context['filter'] = {
            'type': self.request.GET.get('type'),
            'category': self.request.GET.get('category'),
            'order_by': self.request.GET.get('sort', '')
        }

        return context



class QuestionPage(DetailView):
    model = Question
    context_object_name = 'item'
    template_name = 'questions/detail.html'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        object.show_count += 1
        object.save()
        
        context = super(QuestionPage, self).get_context_data(**kwargs)
        
        context['menu'] = 'catalog'
        context['submenu'] = 'questions'
        context['answers'] = Answer.objects.select_related().filter(question=object).order_by('created')

        return context
    
    def post(self, request, *args, **kwargs):
        object = self.get_object()
        answer = Answer(
            parent = None,
            question = object,
            user = self.request.member,
            text = self.request.POST.get('text')
        )
        answer.save()
        
        return redirect(object.url)



class MyQuestionsList(UserListView):
    model = Question
    paginate_by = 10
    template_name = 'questions/my.html'

    def get_queryset(self):
        objects = self.model.objects.filter(user=self.request.member)
        return objects

    def get_context_data(self, **kwargs):
        context = super(MyQuestionsList, self).get_context_data(**kwargs)

        context['menu'] = 'catalog'
        context['submenu'] = 'questions'
        context['types'] = AnimalType.objects.all()
        context['categories'] = Category.objects.all().order_by('order_num')

        return context


class MyQuestionCreate(UserCreateView):
    form_class = QuestionForm
    template_name = 'questions/edit.html'
    success_url = '/questions/my/?success'
    
    def get_context_data(self, **kwargs):
        context = super(MyQuestionCreate, self).get_context_data(**kwargs)

        context['menu'] = 'catalog'
        context['submenu'] = 'questions'
        context['types'] = AnimalType.objects.all()
        context['categories'] = Category.objects.all().order_by('order_num')
        
        return context

    def form_valid(self, form):
        item = form.save(commit=False)
        item.user = self.request.member
        
        # save tags
        #tags = []
        #for tag in request.POST.get('tags', '').split(','):
        #    tag = tag.strip()
        #    if not tag: continue
        #    try:
        #        tag_entity = Tag.objects.get(tag=tag)
        #    except Tag.DoesNotExist:
        #        tag_entity = Tag(tag=tag, count=1)
        #        tag_entity.save()
        #    tags.append(tag_entity.id)
        #item.tags = tags
        
        item.save()
        
        return redirect(self.success_url)


class MyQuestionUpdate(UserUpdateView):
    form_class = QuestionForm
    model = Question
    template_name = 'questions/edit.html'
    success_url = '/questions/my/?success'
    
    def get_context_data(self, **kwargs):
        context = super(MyQuestionUpdate, self).get_context_data(**kwargs)

        context['menu'] = 'catalog'
        context['submenu'] = 'questions'
        context['types'] = AnimalType.objects.all()
        context['categories'] = Category.objects.all().order_by('order_num')
        
        return context


class MyQuestionDelete(UserDeleteView):
    model = Question
    success_url = '/questions/my/'
