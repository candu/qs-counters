from xhpy.pylib import *

from ui.page import :ui:page

from django.http import HttpResponse
from django.shortcuts import redirect

def manage(request):
    page = \
    <ui:page title="Manage Counters">
        <h1>It works!</h1>
    </ui:page>
    return HttpResponse(page)
