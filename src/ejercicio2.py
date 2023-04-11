from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/device/<name>')
def device(name):
    return render_template('device.html')


app.run()
