from xhpy.pylib import *

from ui.js import :ui:js
from ui.page import :ui:page

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect

from qs_counters.models import Counter, Update

import datetime
import json

def _get_duration(presses):
    total = 0
    last_pressed = None
    for press in presses:
        if press.pressed:
            last_pressed = press.timestamp
        elif last_pressed is not None:
            dt = press.timestamp - last_pressed
            total += dt.seconds + 0.000001 * dt.microseconds
            last_pressed = None
    return total

def _get_day_week_metrics(counter):
    now = datetime.datetime.now()
    one_day_ago = now - datetime.timedelta(days=1)
    one_week_ago = now - datetime.timedelta(days=7)
    if counter.type == 'count':
        day_count = Update.objects.filter(
            counter__id=counter.id,
            timestamp__gte=one_day_ago).count()
        week_count = Update.objects.filter(
            counter__id=counter.id,
            timestamp__gte=one_week_ago).count()
        return (day_count, week_count)
    if counter.type == 'duration':
        day_presses = Update.objects.filter(
            counter__id=counter.id,
            timestamp__gte=one_day_ago)
        week_presses = Update.objects.filter(
            counter__id=counter.id,
            timestamp__gte=one_week_ago)
        return (_get_duration(day_presses), _get_duration(week_presses))
    return None

def home(request):
    counters = Counter.objects.all()
    content = <div id="content" />
    for counter in counters:
        day, week = _get_day_week_metrics(counter)
        content_name = \
        <div class="counter-name">{counter.name}</div>
        if counter.pressed:
            content_name.addClass('pressed')
        content_item = \
        <div class="content-item">
            {content_name}
            <div class="counter-stats">
                <div class="stats">
                    <span class="title">day</span>
                    {' '}
                    <span class="count day">{int(round(day))}</span>
                </div>
                <div class="stats">
                    <span class="title">week</span>
                    {' '}
                    <span class="count week">{int(round(week))}</span>
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
        day_count, week_count = _get_day_week_metrics(counter)
        return {
            'success': True,
            'updated': id,
            'day': day_count,
            'week': week_count
        }
    elif counter.type == 'duration':
        counter.pressed = not counter.pressed
        update = Update(
            counter=counter,
            pressed=counter.pressed)
        counter.save()
        update.save()
        day_duration, week_duration = _get_day_week_metrics(counter)
        return {
            'success': True,
            'updated': id,
            'pressed': counter.pressed,
            'day': day_duration,
            'week': week_duration
        }
    return {'success': False}

def update(request, id):
    id = int(id)
    data = _get_update_response(id)
    return HttpResponse(json.dumps(data), content_type='application/json')
