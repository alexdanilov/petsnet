from django.shortcuts import render_to_response
from apps.content.models import Page


def page(request, slug):
    data = {
        'item': Page.objects.get(slug=slug, visibility=True),
    }
    return render_to_response('content/page.html', data)
