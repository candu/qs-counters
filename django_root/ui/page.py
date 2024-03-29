from xhpy.pylib import *
from ui.css import :ui:css
from ui.js import :ui:js

class :ui:page(:x:element):
    attribute string title

    def __init__(self, attributes={}, children=[], source=None):
        super(:ui:page, self).__init__(attributes, children, source)
        self._injected_meta = <x:frag />
        self._injected_js = <x:frag />
        self._injected_css = <x:frag />

    def injectMeta(self, meta):
        self._injected_meta.appendChild(meta)

    def injectJS(self, js):
        self._injected_js.appendChild(js)

    def injectCSS(self, css):
        self._injected_css.appendChild(css)

    def render(self):
        title = self.getAttribute('title')
        head = \
        <head>
            <title>{title}</title>
            <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0" />
            {self._injected_meta}
            <link href="http://fonts.googleapis.com/css?family=Istok+Web:400,700,400italic,700italic" rel="stylesheet" type="text/css" />
            <ui:css path="base.css" />
            {self._injected_css}
            <ui:js path="mootools.js" />
            {self._injected_js}
        </head>
        content = <x:frag />
        for child in self.getChildren():
            content.appendChild(child)
        return \
        <x:doctype>
            <html>
                {head}
                <body>
                    {content}
                </body>
            </html>
        </x:doctype>
