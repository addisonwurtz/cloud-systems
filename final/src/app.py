"""
A simple guestbook flask app.
"""
import flask
from flask.views import MethodView
from index import Index
from add_quote import Sign
from view_entries import ViewEntries

app = flask.Flask(__name__)  # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/add_quote',
                 view_func=Sign.as_view('add_quote'),
                 methods=['GET', 'POST'])

app.add_url_rule('/view_entries',
                 view_func=ViewEntries.as_view('view_entries'),
                 methods=["GET"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
