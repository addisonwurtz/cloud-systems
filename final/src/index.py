from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        """
        Accepts GET requests
        :return: List of dicts of all quote entries in the database
        """
        model = gbmodel.get_model()
        return render_template('index.html')
