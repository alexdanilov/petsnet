import datetime
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import redirect

from apps.announcements.models import *
from apps.content.models import Comment
from apps.users.generic import UserListView, UserCreateView, UserUpdateView, UserDeleteView



class AnnouncementsList(ListView):
    model = Announcement
    paginate_by = 10
    template_name = 'announcements/list.html'

    def get_queryset(self):
        now = datetime.datetime.now()
        objects = self.model.objects.filter(visibility=True, end_date__lte=now)
        
        if self.kwargs.get('type'):
            objects = objects.filter(type=self.kwargs.get('type'))
        if self.request.GET.get('category'):
            objects = objects.filter(category__id=int(self.request.GET.get('category')))
        if self.request.GET.get('q'):
            objects = objects.filter(name__icontains=self.request.GET.get('q'))
        if self.request.GET.get('sort') in ['rating', 'name']:
            objects = objects.order_by(self.request.GET.get('sort'))

        return objects

    def get_context_data(self, **kwargs):
        context = super(AnnouncementsList, self).get_context_data(**kwargs)

        context['menu'] = 'announcements'
        context['submenu'] = 'announcements-%s' % self.kwargs.get('type', 'sale')
        
        context['types'] = TYPE_CHOICES
        context['categories'] = AnnouncementCategory.objects.all()
        context['filter'] = {'order_by': self.request.GET.get('sort', '')}

        items = self.model.objects.filter(visibility=True)
        context['regions'] = items.values('region__region').distinct()

        return context


class AnnouncementPage(DetailView):
    model = Announcement
    context_object_name = 'item'
    template_name = 'announcements/detail.html'

    def get_context_data(self, **kwargs):
        context = super(AnnouncementPage, self).get_context_data(**kwargs)
        object = self.get_object()
        object.show_count += 1
        object.save()
        
        return context


class MyAnnouncementsList(UserListView):
    model = Announcement
    paginate_by = 10
    template_name = 'announcements/my.html'

    def get_queryset(self):
        objects = self.model.objects.filter(user=self.request.member)
        return objects

    def get_context_data(self, **kwargs):
        context = super(MyAnnouncementsList, self).get_context_data(**kwargs)

        context['menu'] = 'announcements'
        context['types'] = TYPE_CHOICES
        context['categories'] = AnnouncementCategory.objects.all()

        return context


class MyAnnouncementCreate(UserCreateView):
    form_class = AnnouncementForm
    template_name = 'announcements/edit.html'
    success_url = '/announcements/my/?success'
    
    def get_context_data(self, **kwargs):
        context = super(MyAnnouncementCreate, self).get_context_data(**kwargs)

        context['menu'] = 'announcements'
        context['types'] = TYPE_CHOICES
        context['categories'] = AnnouncementCategory.objects.all()
        
        return context

    def form_valid(self, form):
        item = form.save(commit=False)
        item.user = self.request.member
        item.end_date = datetime.datetime.now() + datetime.timedelta(days=14)
        item.save()
        
        return redirect(self.success_url)


class MyAnnouncementUpdate(UserUpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcements/edit.html'
    success_url = '/announcements/my/?success'
    
    def get_context_data(self, **kwargs):
        context = super(MyAnnouncementUpdate, self).get_context_data(**kwargs)

        context['menu'] = 'announcements'
        context['types'] = TYPE_CHOICES
        context['categories'] = AnnouncementCategory.objects.all()
        
        return context


class MyAnnouncementDelete(UserDeleteView):
    model = Announcement
    success_url = '/announcements/my/'
    
