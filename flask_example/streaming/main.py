from time import sleep

from flask import Flask, Response, request, stream_with_context

app = Flask(__name__)


@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        sleep(1)
        yield request.args['name']
        sleep(1)
        yield '!'
    return Response(stream_with_context(generate()))


if __name__ == '__main__':
    app.run()
