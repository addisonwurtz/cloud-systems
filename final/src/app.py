"""
A simple guestbook flask app.
"""
import flask
import os
from flask.views import MethodView
from add_contact import Add
from view_contacts import ViewContacts
from tasks import Tasks
from index import Index
from callback import Callback
from logout import Logout

app = flask.Flask(__name__)  # our Flask app

app.secret_key = os.urandom(24)

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/callback',
                 view_func=Callback.as_view('callback'),
                 methods=["GET"])

app.add_url_rule('/add_contact',
                 view_func=Add.as_view('add_contact'),
                 methods=['GET', 'POST'])

app.add_url_rule('/view_contacts',
                 view_func=ViewContacts.as_view('view_contacts'),
                 methods=["GET"])

app.add_url_rule('/view_tasks',
                 view_func=Tasks.as_view('view_tasks'),
                 methods=["GET"])

app.add_url_rule('/logout',
                 view_func=Logout.as_view('logout'),
                 methods=["GET"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
