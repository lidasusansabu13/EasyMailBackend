from flask import Flask, render_template, send_file, jsonify, session
import os
from flask import request
import getTask



app = Flask(__name__)
app.secret_key = 'mysecretkey'


@app.route('/')
def home():
    return render_template('home.html', message='Hello World!')

@app.route('/api/task', methods=['GET'])
def get_todo():
    """
    API to get tasks
    """
    res = getTask.get_tasks()
    return res

@app.route('/api/notification', methods=['GET'])
def get_notification():
    """
    API to get notification
    """
    # API logic goes here
    res = getTask.get_notifications()
    return res

@app.route('/api/events', methods=['GET'])
def get_events():
    """
    API to get events
    """
    res = getTask.get_events()
    return res

# @app.route('/api/others', methods=['GET'])
# def get_others():
#     """
#     API to get events
#     """
#     res = getTask.get_others()
#     return res


@app.route('/api/breakdown', methods=['POST'])
def breakdown_email():
    """
    ha
    """
    content = request.form.to_dict()
    response = getTask.main(content["content"])
    # API logic goes here
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
