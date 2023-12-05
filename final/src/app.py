"""
A simple guestbook flask app.
"""
import flask
from flask.views import MethodView

from add_contact import Add
from view_contacts import ViewContacts
from index import Index

app = flask.Flask(__name__)  # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/add_contact',
                 view_func=Add.as_view('add_contact'),
                 methods=['GET', 'POST'])

app.add_url_rule('/view_contacts',
                 view_func=ViewContacts.as_view('view_contacts'),
                 methods=["GET"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
