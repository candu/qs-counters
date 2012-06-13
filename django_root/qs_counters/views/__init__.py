from xhpy.pylib import *

from ui.js import :ui:js
from ui.page import :ui:page

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect

from qs_counters.models import Counter, Update

import json

def home(request):
    counters = Counter.objects.all()
    content = <div id="content" />
    for counter in counters:
        content_item = <div class="content-item">{counter.name}</div>
        content_item.setAttribute('id', 'counter-{0}'.format(counter.id))
        if counter.pressed:
            content_item.addClass('pressed')
        content.appendChild(content_item)
    if len(counters) < 5:
        add_counter = \
        <div class="add-counter">
            <a href="/add">+</a>
        </div>
        content.appendChild(add_counter)
    page = \
    <ui:page title="counters">
    <div id="container">
        <div id="header">
            counters
        </div>
        {content}
    </div>
    </ui:page>
    page.injectJS(<ui:js path="home.js" />)
    return HttpResponse(page)

def add(request):
    if request.POST:
        print 'POST data received'
        counter = Counter(
            name=request.POST['name'],
            type=request.POST['type'])
        counter.save()
        return redirect('/')
    csrf_token = unicode(csrf(request)['csrf_token'])
    page = \
    <ui:page title="add counter">
    <div id="container">
        <div id="header">
            add counter
        </div>
        <div id="content">
            <form action="/add" method="post">
            <div class="form-row hidden">
                <input type="hidden" name="csrfmiddlewaretoken" id="csrfmiddlewaretoken" value={csrf_token} />
            </div>
            <div class="form-row">
                <input name="name" id="name" placeholder="counter name" />
            </div>
            <div class="form-row">
                <label for="type">count</label>
                <input type="radio" name="type" value="count" checked={True} />
                <label for="type">duration</label>
                <input type="radio" name="type" value="duration" />
            </div>
            <div class="form-row">
                <input type="submit" value="add" />
            </div>
            </form>
        </div>
    </div>
    </ui:page>
    return HttpResponse(page)

def delete(request):
    pass

def _get_update_response(id):
    try:
        counter = Counter.objects.get(id=id)
    except Counter.DoesNotExist:
        return {'success': False}
    update = Update(counter=counter)
    update.save()
    if counter.type == 'count':
        return {'success': True, 'updated': id}
    elif counter.type == 'duration':
        counter.pressed = not counter.pressed
        counter.save()
        return {'success': True, 'updated': id, 'pressed': counter.pressed}
    return {'success': False}

def update(request, id):
    id = int(id)
    print id
    data = _get_update_response(id)
    return HttpResponse(json.dumps(data), content_type='application/json')
