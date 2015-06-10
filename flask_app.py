'''
Under MIT License. Please see accompanying LICENSE document.
'''
import re
import flask
import argparse
import bongy

# The Web interface
app = flask.Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return flask.render_template('index.html')

@app.route('/api/v1/<text>')
def api_v1(text):
    conv = bongy.Converter()
    return conv.convert(text)

@app.route('/mappings')
def api_v1_mappings():
    conv = bongy.Converter()
    return conv.gen_mapping()

# MAIN

def start_server(port=8084):
    app.run(port=port)

if __name__ == '__main__':
    aparser = argparse.ArgumentParser(description='Start bongy in server mode')
    aparser.add_argument('-p', '--port', help='Specify port for the server, default 8084')
    args = aparser.parse_args()

    if args.port:
        start_server(port=int(args.port))
    else:
        start_server()
