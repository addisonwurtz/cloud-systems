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
        contacts = [dict(first_name=row[0], last_name=row[1], orbit=row[2], contact_history=row[3], date_added=row[4]) for row in model.select()]
        return render_template('index.html', contacts=contacts)
