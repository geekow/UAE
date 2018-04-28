from flask import Flask
from gevent.wsgi import WSGIServer
from logging import handlers
import logging
import sys

file_handler = handlers.TimedRotatingFileHandler(filename='./logs/backend.logs', when='midnight', interval=1)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s'))

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
ch.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(ch)

app = Flask(__name__)
app.config.update(DEBUG=True)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/about')
def about():
    return 'UAE Challenge backend at 42'


logger.info('Launching web server on port 5000')
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
