from flask import current_app, make_response, url_for
from jinja2 import Markup
import re, json

JSGLUE_JS_PATH = '/jsglue.js'
JSGLUE_NAMESPACE = 'Flask'
rule_parser = re.compile(r'<(.+?)>')
splitter = re.compile(r'<.+?>')


def get_routes(app):
    output = []
    for r in app.url_map.iter_rules():
        endpoint = r.endpoint
        rule = r.rule
        rule_args = [x.split(':')[-1] for x in rule_parser.findall(rule)]
        rule_tr = splitter.split(rule)
        output.append((endpoint, rule_tr, rule_args))
    return sorted(output, key=lambda x: len(x[1]), reverse=True)


class JSGlue(object):
    def __init__(self, app=None, **kwargs):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        @app.route(JSGLUE_JS_PATH)
        def serve_js():
            return make_response(
                (self.generate_js(), 200, {'Content-Type': 'text/javascript'})
            )

        @app.context_processor
        def context_processor():
            return {'JSGlue': JSGlue}

    def generate_js(self):
        rules = get_routes(self.app)
        with open('glue.js') as gluefile:
            jsfmtstr = gluefile.read()
            return jsfmtstr % (JSGLUE_NAMESPACE, json.dumps(rules))

    @staticmethod
    def include():
        js_path = url_for('serve_js')
        return Markup('<script src="%s" type="text/javascript"></script>') % (js_path,)
