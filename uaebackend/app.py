from flask import Flask, request
from collections import Counter
from gevent.wsgi import WSGIServer
from uaebackend import config
from pymongo import MongoClient
from logging import handlers
import logging
import json
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

MONGO_CLIENT = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
MONGO_DB = MONGO_CLIENT['UAE']


@app.route('/')
def index():
    return 'Index Page'


@app.route('/add_user_trad_word', methods=['POST'])
def user_trad():
    try:
        content = request.get_json(force=True)
        if 'arabic' not in content or 'english' not in content:
            return json.dumps({'status': 'error', 'message': 'Missing key(s) in JSON'})
        # Treating arabic collections
        result = MONGO_DB['ARABIC'].find_one({'word': content['arabic']})
        if not result:
            arabic = {'word': content['arabic'], 'translations': [content['english']]}
            MONGO_DB['ARABIC'].insert_one(arabic)
            logger.info('Successfully added translation to arabic collection')
        else:
            translations = result['translations']
            translations.append(content['english'])
            MONGO_DB['ARABIC'].update_one({'_id': result['_id']}, {'$set': {'translations': translations}},
                                          upsert=False)
            logger.info('Successfully updated translation to arabic collection')
        # Treating english connections
        result = MONGO_DB['ENGLISH'].find_one({'word': content['english']})
        if not result:
            english = {'word': content['english'], 'translations': [content['english']]}
            MONGO_DB['ENGLISH'].insert_one(english)
            logger.info('Successfully added translation to english collection')
        else:
            translations = result['translations']
            translations.append(content['arabic'])
            MONGO_DB['ENGLISH'].update_one({'_id': result['_id']}, {'$set': {'translations': translations}},
                                           upsert=False)
            logger.info('Successfully updated translation to english collection')
        return json.dumps({'status': 'success'})
    except Exception as e:
        logger.warning('Unhandled exception: %s', e)
        return json.dumps({'status': 'error', 'message': 'Unhandled exception, well done jjacobi !'})


@app.route('/ask_traduction/<language>/<word>', methods=['GET'])
def ask_trad(language, word):
    language = str(language).upper()
    word = str(word)
    if language != 'ARABIC' and language != 'ENGLISH':
        logger.warning('User attempt to translate from %s', language)
        return json.dumps({'status': 'error', 'message': 'Language not valid'})
    result = MONGO_DB['ARABIC' if language == 'ENGLISH' else 'ENGLISH'].find_one({'word': word})
    if not result:
        logger.warning('User asked for non existing translation for %s in %s', word, language)
        if not MONGO_DB['TOTRADUCE'].find_one({'word': word, 'traduce_in': language}):
            MONGO_DB['TOTRADUCE'].insert_one({'word': word, 'traduce_in': language})
        return json.dumps({'status': 'error',
                           'message': 'We have no translation for {word} in {language} for the moment'
                          .format(word=word, language=language)})
    # Now return most common translation
    word_counter = Counter(result['translations'])
    logger.info('Sending translation for %s in %s : %s', word, language, word_counter.most_common(1))
    return json.dumps({'status': 'success', 'result': word_counter.most_common(1)[0]})


@app.route('/get_word_to_traduce/<language>')
def get_word_to_traduce(language):
    language = str(language).upper()
    language = 'ARABIC' if language == 'ENGLISH' else 'ENGLISH'
    result = MONGO_DB['TOTRADUCE'].find_one({'traduce_in': language})
    if not result:
        logger.warning('We habe no word to traduce in %s', language)
        return json.dumps({'status': 'error', 'message': 'We have no word to traduce in ' + str(language)})
    MONGO_DB['TOTRADUCE'].remove(result)
    logger.info('Sending %s to traduce in %s', result['word'], result['traduce_in'])
    return json.dumps({'status': 'success', 'word': result['word']})


@app.route('/about')
def about():
    return 'UAE Challenge backend at 42'


logger.info('Launching web server on port 5000')
http_server = WSGIServer(('', config.WEB_SERVER_PORT), app)
http_server.serve_forever()
