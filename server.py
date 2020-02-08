#!/usr/bin/env python
# Based on https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

import argparse
import logging
import os

from flask import Flask
from flask import Response
from flask import abort
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import request
from flask_httpauth import HTTPBasicAuth

from utils import setup_logging

PORT = 'port'
LOG_LEVEL = 'loglevel'

logger = logging.getLogger(__name__)

auth = HTTPBasicAuth()
http = Flask(__name__)


@auth.get_password
def get_password(username):
    if username == 'top':
        return 'secret'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@http.route('/')
def root():
    return Response('This is a really cool app', mimetype='text/plain')


@http.route('/plain-hello')
def plain_hello():
    return Response('Hello World!', mimetype='text/plain')


@http.route('/html-hello')
def html_hello():
    text = '''
    <html>
        <head>
        </head>
        <body>
            <h1>Hello World!</h1>
            <h2>Hello World!</h2>
            <h3>Hello World!</h3>
            <h4>Hello World!</h4>
        </body>
    </html>
    '''
    return Response(text, mimetype='text/html')


counter = 0

@http.route("/template")
def template():
    global counter
    counter = counter + 1
    message = "Hello, World " + str(counter)
    return render_template('template.html', message=message)


def main():
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', dest=PORT, default=8080, help='HTTP port [8080]')
    parser.add_argument('-v', '--verbose', dest=LOG_LEVEL, default=logging.INFO, action='store_const',
                        const=logging.DEBUG, help='Enable debugging info')
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    port = int(os.environ.get('PORT', args[PORT]))
    logger.info("Starting server listening on port {}".format(port))
    http.run(debug=False, port=port, host='0.0.0.0')


if __name__ == "__main__":
    main()