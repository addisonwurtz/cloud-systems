from flask import render_template
from flask.views import MethodView
import gbmodel

class ViewContacts(MethodView):
    def get(self):
        """
        Retrieves all contact entries from database
        :return: List of dicts containing contact data
        """
        model = gbmodel.get_model()
        contacts = [dict(first_name=row[0], last_name=row[1], orbit=row[2], contact_history= row[3], date_added=row[4] ) for row in model.select()]
        return render_template('view_contacts.html', contacts=contacts)
