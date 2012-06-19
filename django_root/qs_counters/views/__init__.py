from xhpy.pylib import *

from ui.js import :ui:js
from ui.css import :ui:css
from ui.page import :ui:page

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect

from lib.metrics import Metrics
from qs_counters.models import Counter, Update

import json
import time

MAX_COUNTERS = 5

def home(request):
    counters = Counter.objects.all()
    content = <div id="content" />
    for counter in counters:
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
    if len(counters) < MAX_COUNTERS:
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
    page.injectJS(<ui:js path="base.js" />)
    page.injectJS(<ui:js path="home.js" />)
    page.injectCSS(<ui:css path="home.css" />)
    return HttpResponse(page)

def add(request):
    num_counters = Counter.objects.all().count()
    if num_counters >= MAX_COUNTERS:
        return redirect('/')
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

def view(request, id):
    counter = Counter.objects.get(id=id)
    if counter.type == 'count':
        action_name = 'bump'
    elif counter.pressed:
        action_name = 'stop'
    else:
        action_name = 'start'
    page = \
    <ui:page title="counters">
    <div id="container">
        <div id="header">
           {counter.name}
        </div>
        <div id="content">
            <div class="counter-stats">
                <div class="stats">
                    <div class="label day">day</div>
                    <div class="count day">loading...</div>
                </div>
                <div class="stats">
                    <div class="label week">week</div>
                    <div class="count week">loading...</div>
                </div>
            </div>
            <div class="actions">
                <form action={'/update/{0}'.format(id)} method="get">
                    <input type="hidden" id="counter_id" name="counter_id" value={id} />
                    <input type="submit" id="update" name="action" value={action_name} />
                    <input type="submit" id="cancel" name="action" value="cancel" />
                </form>
            </div>
        </div>
    </div>
    </ui:page>
    page.injectJS(<ui:js path="base.js" />)
    page.injectJS(<ui:js path="view.js" />)
    page.injectCSS(<ui:css path="view.css" />)
    return HttpResponse(page)

def update(request, id):
    action = request.GET.get('action')
    if action is None or action == 'cancel':
        return redirect('/')
    id = int(id)
    counter = Counter.objects.get(id=id)
    if counter.type == 'count':
        update = Update(counter=counter)
        update.save()
    else:
        counter.pressed = not counter.pressed
        update = Update(
            counter=counter,
            pressed=counter.pressed)
        counter.save()
        update.save()
    return redirect('/')

def delete(request, id):
    pass

def _get_stats(counter):
    day_stats, week_stats = Metrics.getMetrics(counter)
    try:
        last = Update.objects.filter(counter__id=counter.id).order_by('id').reverse()[0]
        print last.timestamp
        last = time.mktime(last.timestamp.timetuple())
    except IndexError:
        last = None
    print last
    return {
        'pressed': counter.pressed,
        'id': counter.id,
        'type': counter.type,
        'day': day_stats,
        'week': week_stats,
        'last': last
    }

def stats_all(request):
    stats = dict((c.id, _get_stats(c)) for c in Counter.objects.all())
    return HttpResponse(json.dumps(stats), content_type='application/json')

def stats(request, id):
    stats = _get_stats(Counter.objects.get(id=id))
    return HttpResponse(json.dumps(stats), content_type='application/json')
