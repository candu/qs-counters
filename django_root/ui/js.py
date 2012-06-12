from xhpy.pylib import *

from django.conf import settings

class :ui:js(:x:element):
    attribute string path
    def render(self):
        path = self.getAttribute('path')
        return <script type="text/javascript" src={settings.STATIC_URL + path} />
