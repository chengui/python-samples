from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello'

@app.route('/echo')
def echo():
    text = request.args.get('text', '')
    app.logger.error('echo: %s', text)
    return text

if __name__ == '__main__':
    app.run(port=8080)
