from xhpy.pylib import *

from ui.js import :ui:js
from ui.page import :ui:page

from django.http import HttpResponse
from django.shortcuts import redirect

def manage(request):
    page = \
    <ui:page title="Manage Counters">
    <div id="container">
        <div id="header">
            manage counters
        </div>
        <div id="content">
            <div class="content-item">+</div>
            <div class="content-item">test</div>
        </div>
    </div>
    </ui:page>
    page.injectJS(<ui:js path="manage.js" />)
    return HttpResponse(page)
