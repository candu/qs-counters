from xhpy.pylib import *

from ui.js import :ui:js
from ui.page import :ui:page

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect

from qs_counters.models import Counter, Update

def home(request):
    counters = Counter.objects.all()
    content = <div id="content" />
    for counter in counters:
        content_item = <div class="content-item">{counter.name}</div>
        content.appendChild(content_item)
    if len(counters) < 5:
        add_counter = \
        <div class="content-item">
            <div class="add"><a href="/add">+</a></div>
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
        data = {'type': request.POST['type']}
        daily_min = request.POST['daily_min']
        if daily_min:
            data['daily_min'] = int(daily_min)
        daily_max = request.POST['daily_max']
        if daily_max:
            data['daily_max'] = int(daily_max)
        weekly_min = request.POST['weekly_min']
        if weekly_min:
            data['weekly_min'] = int(weekly_min)
        weekly_max = request.POST['weekly_max']
        if weekly_max:
            data['weekly_max'] = int(weekly_max)
        counter = Counter(name=request.POST['name'], data=data)
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
                <label for="daily_min">daily min</label>
                <input type="number" name="daily_min" id="daily_min" />
                <label for="daily_max">max</label>
                <input type="number" name="daily_max" id="daily_max" />
            </div>
            <div class="form-row">
                <label for="weekly_min">weekly min</label>
                <input type="number" name="weekly_min" id="weekly_min" />
                <label for="weekly_max">max</label>
                <input type="number" name="weekly_max" id="weekly_max" />
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

def update(request):
    pass

def stats(request):
    pass
