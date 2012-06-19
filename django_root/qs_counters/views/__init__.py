from xhpy.pylib import *

from ui.js import :ui:js
from ui.page import :ui:page

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect

from lib.metrics import Metrics
from qs_counters.models import Counter, Update

import json

def home(request):
    counters = Counter.objects.all()
    content = <div id="content" />
    for counter in counters:
        day, week = Metrics.getMetrics(counter)
        counter_name = \
        <div class="counter-name">{counter.name}</div>
        if counter.pressed:
            counter_name.addClass('pressed')
        content_item = \
        <div class="content-item">
            {counter_name}
            <div class="counter-stats">
                <div class="stats">
                    <span class="count day">loading...</span>
                </div>
            </div>
        </div>
        content_item.setAttribute('id', 'counter-{0}'.format(counter.id))
        content_item.addClass(counter.type)
        content.appendChild(content_item)
    if len(counters) < 5:
        add_counter = \
        <a href="/add">
            <div class="content-item add">+</div>
        </a>
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
    if counter.type == 'count':
        update = Update(counter=counter)
        update.save()
        day_count, week_count = Metrics.getMetrics(counter)
        return {
            'success': True,
            'updated': id,
            'day': day_count,
        }
    elif counter.type == 'duration':
        counter.pressed = not counter.pressed
        update = Update(
            counter=counter,
            pressed=counter.pressed)
        counter.save()
        update.save()
        day_duration, week_duration = Metrics.getMetrics(counter)
        return {
            'success': True,
            'updated': id,
            'pressed': counter.pressed,
            'day': day_duration,
        }
    return {'success': False}

def update(request, id):
    id = int(id)
    data = _get_update_response(id)
    return HttpResponse(json.dumps(data), content_type='application/json')

def stats_all(request):
    stats = {}
    counters = Counter.objects.all()
    for counter in counters:
        day_stats, week_stats = Metrics.getMetrics(counter)
        stats[counter.id] = {
            'pressed': counter.pressed,
            'id': counter.id,
            'type': counter.type,
            'day': day_stats,
            'week': week_stats
        }
    return HttpResponse(json.dumps(stats), content_type='application/json')
