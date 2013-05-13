from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from apps.photoalbums.models import *



def my(request):
    page = request.GET.get('page', 1)
    objects = Album.objects.select_related().filter(user=request.member).order_by('-created')
    paginator = Paginator(objects, 10)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    data = {
        'items': items,
        'user_menu': 'list',
        'start_index': items.start_index(),
        'end_index': items.end_index(),
    }
    return render_to_response('photoalbums/my.html', data, context_instance=RequestContext(request))


def edit(request, id=None):
    item = {} if not id else Album.objects.select_related().get(pk=id, user=request.member)
    data = {
        'item': item,
        'user_menu': 'edit',
    }
    data.update(csrf(request))

    if request.method == 'POST':
        if id:
            form = AlbumForm(request.POST, instance=item)
        else:
            form = AlbumForm(request.POST)
            data['item'] = request.POST

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.member
            if not item.id:
                item.show_count = 0
                item.comments_count = 0
            item.save()
            return redirect('/my/photos/?result=success')
        else:
            data['errors'] = form.errors
            data['result'] = 'failed'

    return render_to_response('photoalbums/edit.html', data, context_instance=RequestContext(request))


def delete(request, id=None):
    if id:
        Album.objects.get(pk=id, user=request.member).delete()

    return redirect('/my/photos/?result=success')


def list(request):
    objects = Post.objects.select_related().all().order_by('-created')
    paginator = Paginator(objects, 10)
    try:
        items = paginator.page(request.GET.get('page', 1))
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    data = {
        'items': items,
        'top_menu': 'interesting',
        'top_menu_sub': 'blogs',
        'entity_url': '/blogs/',
        'start_index': items.start_index(),
        'end_index': items.end_index(),
    }
    return render_to_response('photoalbums/list.html', data, context_instance=RequestContext(request))


def show(request, id=None):
    item = Post.objects.select_related().get(pk=id)

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
    data = {
        'item': item,
        'comments': Comment.objects.select_related().filter(post__id=id).order_by('-created'),
        'top_menu': 'interesting',
        'top_menu_sub': 'blogs',
        'entity_url': '/blogs/',
    }
    return render_to_response('photoalbums/item.html', data, context_instance=RequestContext(request))