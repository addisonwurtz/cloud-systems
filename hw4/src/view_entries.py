from flask import render_template
from flask.views import MethodView
import gbmodel

class ViewEntries(MethodView):
    def get(self):
        """
        Retrieves all quote entries from database
        :return: List of dicts containing quote data
        """
        model = gbmodel.get_model()
        entries = [dict(quote=row[0], attribution=row[1], rating=row[2], date_added=row[3] ) for row in model.select()]
        return render_template('view_entries.html', entries=entries)
