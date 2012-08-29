import datetime
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from apps.animals.models import Animal
from apps.blogs.models import Comment, Post
from apps.users.models import *



def animals(request, user=None):
    user = UserProfile.objects.get(pk=user)
    data = {
        'user': user,
    }

    paginator = Paginator(Animal.objects.filter(user=user), 10)
    try:
        data['items'] = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        data['items'] = paginator.page(1)
    except EmptyPage:
        data['items'] = paginator.page(paginator.num_pages)

    return render_to_response('users/user-animals.html', data, context_instance=RequestContext(request))


def blog_list(request, user=None):
    user = UserProfile.objects.get(pk=user)
    data = {
        'user': user,
    }

    paginator = Paginator(Post.objects.filter(user=user).order_by('-created'), 10)
    try:
        data['items'] = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        data['items'] = paginator.page(1)
    except EmptyPage:
        data['items'] = paginator.page(paginator.num_pages)

    return render_to_response('users/user-blog.html', data, context_instance=RequestContext(request))


def blog_show(request, user, post):
    user = UserProfile.objects.get(pk=user)
    item = Post.objects.get(pk=post, user=user)
    data = {
        'user': user,
        'item': item
    }
    if request.member and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.member
            comment.post = item
            comment.save()
            item.comments_count += 1
            item.save()
            return redirect('?')

    item.show_count += 1
    item.save()

    data['comments'] = Comment.objects.select_related().filter(post=item).order_by('-created')
    return render_to_response('users/user-post.html', data, context_instance=RequestContext(request))


def friends(request, user=None):
    user = UserProfile.objects.get(pk=user)
    data = {
        'user': user
    }

    paginator = Paginator(UserFriend.objects.filter(user=user, accept=True), 10)
    try:
        data['items'] = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        data['items'] = paginator.page(1)
    except EmptyPage:
        data['items'] = paginator.page(paginator.num_pages)

    return render_to_response('users/user-friends.html', data, context_instance=RequestContext(request))


def meetings(request, user=None):
    user = UserProfile.objects.get(pk=user)
    data = {
        'user': user
    }

    ids = [x.meeting.id for x in MeetingMember.objects.filter(user=user)]
    paginator = Paginator(Meeting.objects.filter(id__in=ids), 10)
    try:
        data['items'] = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        data['items'] = paginator.page(1)
    except EmptyPage:
        data['items'] = paginator.page(paginator.num_pages)

    return render_to_response('users/user-meetings.html', data, context_instance=RequestContext(request))


def photos(request):
    user = UserProfile.objects.get(pk=user)
    data = {
        'user': user
    }

    paginator = Paginator(UserFriend.objects.filter(user=data['user'], accept=True), 10)
    try:
        data['items'] = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        data['items'] = paginator.page(1)
    except EmptyPage:
        data['items'] = paginator.page(paginator.num_pages)

    return render_to_response('users/user-photoalbums.html', data, context_instance=RequestContext(request))


def profile(request, user=None):
    now = datetime.datetime.now().date()
    user = UserProfile.objects.get(pk=user)

    if request.member and request.POST.has_key('addwall'):
        row = UserWall(
            user=user,
            author=request.member,
            message=request.POST.get('message')
        )
        row.save()
        return redirect('/users/%s' % user.id)

    data = {
        'user': user,
        'user_menu': 'profile',
        'animals': Animal.objects.filter(user=user, visibility=True, deleted=False)[0:3],
        'blog_posts': Post.objects.filter(user=user).order_by('-created')[0:3],
        'friends': UserFriend.objects.filter(user=user, accept=True).order_by('?')[0:3],
        'meetings': Meeting.objects.filter(user=user, begin_date__gte=now).order_by('begin_date')[0:3],
        'photos': UserWall.objects.filter(user=user).order_by('-created')[0:3],
        'wall': UserWall.objects.filter(user=user).order_by('-created')[0:3],
    }
    data.update(csrf(request))

    return render_to_response('users/user-profile.html', data, context_instance=RequestContext(request))
