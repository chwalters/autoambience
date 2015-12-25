from autoambience.KeywordIdentifier import KeywordIdentifier
from flask import Flask

ki = KeywordIdentifier()
app = Flask(__name__)

@app.route('/')
def nothing_interesting():
    return '"launch" flask application running'

@app.route('/process/<text>')
def process(text):
    return ki.process(text)


if __name__ == '__main__':
    app.run()
