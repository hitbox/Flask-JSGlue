#from __future__ import absolute_import

from flask import Flask, render_template_string
from werkzeug.wsgi import DispatcherMiddleware

import flask_jsglue

app = Flask(__name__)
flask_jsglue.JSGlue(app)

#app.config['APPLICATION_ROOT'] = '/jsglue'

def simple(env, resp):
    resp(b'200 OK', [(b'Content-Type', b'text/plain')])
    return [b'Hello WSGI World']

app.wsgi_app = DispatcherMiddleware(simple, {'/jsglue': app.wsgi_app})

@app.route('/')
def index():
    return render_template_string('''
    {{ JSGlue.include() }}
    <h1>Hello!</h1>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
