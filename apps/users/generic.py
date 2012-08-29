from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect


class UserListView(ListView):
    "Mixin class for check user auth and provider ListView interface"
    
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['member'] = self.request.member
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.member:
            return redirect('/account/signin/')
            
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserDetailView(DetailView):
    "Mixin class for check user auth and provider DetailView interface"
    
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['member'] = self.request.member
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.member:
            return redirect('/account/signin/')
            
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    "Mixin class for check user auth and provider CreateView interface"
    
    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['member'] = self.request.member
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not equest.member:
            return redirect('/account/signin/')
            
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    "Mixin class for check user auth and provider UpdateView interface"
    
    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['member'] = self.request.member
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.member:
            return redirect('/account/signin/')
            
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    
    def get(self, request, *args, **kwargs):
        try:
            object = self.model.objects.get(pk=kwargs['pk'])
            object.delete()
        except Exception:
            pass
        
        return redirect(self.success_url)
