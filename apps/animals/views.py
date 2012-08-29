import datetime
import urllib

from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from apps.animals.models import *
from apps.content.models import Comment
from apps.system.models import Regions
from apps.system.views import get_monthes


def list(request):
    page = request.GET.get('page', 1)
    items_filter = {
        'visibility': True,
        'deleted': False,
    }

    # filters
    filter = {}
    for field in ('age__lte', 'age__lte'):
        if request.GET.has_key(field) and request.GET[field]:
            filter[field] = request.GET[field]

    items_filter.update(filter)

    # try to find region
    try:
        region = Regions.objects.get(pk=int(request.GET.get('region_id', 0)))
        items_filter['region'] = region
        filter['region'] = region.city_name_ru
    except: pass

    # try to find breed
    try:
        breed = Breed.objects.get(pk=int(request.GET.get('breed_id', 0)))
        items_filter['breed'] = breed
        filter['breed'] = breed.name
    except: pass

    # get filtered items
    objects = Animal.objects.select_related().filter(**items_filter)

    # filter by search text
    if request.GET.has_key('q') and request.GET['q']:
        filter['q'] = request.GET['q']
        objects = objects.filter(Q(title__icontains=request.GET['q']), Q(description__icontains=request.GET['q']))

    paginator = Paginator(objects, 10)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    data = {
        'items': items,
        'filter': filter,
        'user_menu': 'animals',
        'start_index': items.start_index(),
        'end_index': items.end_index(),
        'url': urllib.urlencode(filter),
    }
    return render_to_response('animals/animals-list.html', data, context_instance=RequestContext(request))


def show(request, id):
    item = Animal.objects.select_related().get(pk=id, visibility=True, deleted=False)

    filter = {}
    for field in ('age__lte', 'age__lte', 'q', 'region_id', 'breed_id'):
        if request.GET.has_key(field) and request.GET[field]:
            filter[field] = request.GET[field]

    if request.member and request.GET.has_key('add-comment'):
        new_comment = Comment(**{
            'entity': 'animals',
            'id_entities': item.id,
            'user': request.member,
            'comment': request.POST['comment'],
            'visibility': True,
        })
        new_comment.save()
        return redirect('?')

    data = {
        'item': item,
        'filter': filter,
        'url': urllib.urlencode(filter),
        'other': Animal.objects.select_related().filter(visibility=True, deleted=False).exclude(pk=item.id)[0:3],
        'comments': Comment.objects.select_related().filter(entity='animals', id_entities=item.id, visibility=True).order_by('-created')[0:3]
    }
    return render_to_response('animals/animals-item.html', data, context_instance=RequestContext(request))


def ajax_get_breeds(request):
    objects = Breed.objects.filter(name__icontains=request.GET.get('q', ''))
    output = "\n".join(['%s|%s' % (o.id, o.name) for o in objects])
    return HttpResponse(output)


def my(request):
    page = request.GET.get('page', 1)
    objects = Animal.objects.select_related().filter(user=request.member, deleted=False)
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
    return render_to_response('animals/animals-my.html', data, context_instance=RequestContext(request))


def edit(request, id=None):
    item = {} if not id else Animal.objects.select_related().get(pk=id, deleted=False)

    data = {
        'item': item,
        'user_menu': 'edit',
        'types': AnimalType.objects.all(),
        'genders': ANIMAL_GENDERS,
        'days': range(1, 31),
        'monthes': get_monthes(True),
        'years': range(datetime.datetime.now().year, 1970, -1)
    }
    data.update(csrf(request))

    if request.method == 'POST':
        if id:
            form = AnimalForm(request.POST, instance=item)
        else:
            form = AnimalForm(request.POST)
            data['item'] = request.POST
            
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.member
            item.region = request.member.region
            item.visibility = True
            item.birth_day = '%s-%s-%s' % (request.POST.get('year'), request.POST.get('month'), request.POST.get('day'))
            item.save()
            
            for i in range(1, 4):
                if request.FILES.has_key('image%s' % i):
                    img = AnimalImage(animal=item, image=request.FILES['image%s' % i])
                    img.save()
            
            return redirect('/my/animals/?result=success')
        else:
            data['errors'] = form.errors
            data['result'] = 'failed'

    return render_to_response('animals/animals-edit.html', data, context_instance=RequestContext(request))


def delete(request, id=None):
    if id:
        Animal.objects.get(pk=id, user=request.member).delete()

    return redirect('/my/animals/?result=success')
