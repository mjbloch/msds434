from flask import Flask, render_template
import json


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download')
def download():
    data = {'message': 'Hello, world!'}
    json_data = json.dumps(data)

    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=data.json'}
    )

    return response


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)