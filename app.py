from flask import Flask, render_template, request
import socket
from client import clientFun

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    return clientFun(message)

if __name__ == '__main__':
    app.run(debug=True)