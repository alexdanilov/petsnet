import datetime
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _

from apps.animals.models import Animal
from apps.announcements.models import Announcement
from apps.blogs.models import Post
from apps.users.models import *
from apps.system.views import get_monthes



def home(request):
    now = datetime.datetime.now().date()
    data = {
        'user': request.member,
        'animals': Animal.objects.filter(user=request.member)[0:5],
        'announcements': Announcement.objects.filter(user=request.member).order_by('created')[0:3],
        'blog_posts': Post.objects.filter(user=request.member).order_by('created')[0:3],
        'friends': UserFriend.objects.filter(Q(user=request.member) | Q(friend=request.member)).filter(accept=True)[0:5],
    }
    return render_to_response('users/my-home.html', data, context_instance=RequestContext(request))



def friends(request):
    waiting_friends = UserFriend.objects.filter(Q(user=request.member) | Q(friend=request.member))
    data = {
        'user': request.member,
        'waiting_users': waiting_friends.filter(accept=False)
    }

    paginator = Paginator(waiting_friends.filter(accept=True), 10)
    try:
        data['items'] = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        data['items'] = paginator.page(1)
    except EmptyPage:
        data['items'] = paginator.page(paginator.num_pages)

    return render_to_response('users/my-friends.html', data, context_instance=RequestContext(request))


@csrf_exempt
def ajax_friend_add(request, friend):
    try:
        friend = UserProfile.objects.get(pk=friend)
        relation = UserFriend(user=request.member, friend=friend, accept=True)
        relation.save()
        result = _('friend-added')
    except Exception:
        result = _('friend-added-yet')
    return HttpResponse(result)


@csrf_exempt
def ajax_friend_delete(request):
    if request.POST.has_key('id') and request.POST['id']:
        try:
            UserFriend.objects.get(pk=id, user=request.member).delete()
            return HttpResponse('1')
        except Exception:
            pass
    return HttpResponse('0')


def messages(request):
    data = {
        'user': request.member
    }

    messages = UserMessage.objects.filter(Q(user=request.member) | Q(author=request.member)).order_by('-readed', '-created')
    paginator = Paginator(messages, 10)
    try:
        data['items'] = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        data['items'] = paginator.page(1)
    except EmptyPage:
        data['items'] = paginator.page(paginator.num_pages)

    return render_to_response('users/my-messages.html', data, context_instance=RequestContext(request))


def message_new(request):
    data = {
        'user': request.member
    }
    if request.GET.get('to'):
        data['recepient'] = UserProfile.objects.get(pk=request.GET.get('to'))
    
    return render_to_response('users/my-new-message.html', data, context_instance=RequestContext(request))

def show_dialog(request, user_id=None):
    data = {
       'user': request.member
    }

    messages = UserMessage.objects.filter(Q(user=request.member, to_user__id=user_id) | Q(to_user=request.member, user__id=user_id)).order_by('-created')
    paginator = Paginator(messages, 20)
    try:
        data['items'] = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        data['items'] = paginator.page(1)
    except EmptyPage:
        data['items'] = paginator.page(paginator.num_pages)
    
    return render_to_response('users/my-show-dialog.html', data, context_instance=RequestContext(request))


def settings(request):
    data = {
        'user': request.member,
        'user_menu': 'settings',
        'genders': GENDER_CHOICES,
        'days': range(1, 31),
        'monthes': get_monthes(True),
        'years': range(datetime.datetime.now().year, 1970, -1)
    }
    data.update(csrf(request))

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.member)
        if form.is_valid():
            user = form.save(commit=False)
            if request.FILES.get('avatar'):
                user.avatar_file = request.FILES['avatar']
            #user.birth_day = '%s-%s-%s' % (request.POST.get('year'), request.POST.get('menth'), request.POST.get('day'))
            user.save()
        else:
            data['errors'] = form.errors

    data['item'] = UserProfile.objects.get(pk=request.member.id)
    return render_to_response('users/my-settings.html', data, context_instance=RequestContext(request))
