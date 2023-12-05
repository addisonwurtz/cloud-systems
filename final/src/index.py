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
        entries = [dict(quote=row[0], attribution=row[1], rating=row[2], date_added=row[3] ) for row in model.select()]
        return render_template('index.html',entries=entries)
