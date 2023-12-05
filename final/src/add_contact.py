from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Add(MethodView):
    def get(self):
        """
        :return: form template for adding new contacts
        """
        return render_template('add_contact.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        model = gbmodel.get_model()
        model.insert(request.form['first_name'], request.form['last_name'], request.form['orbit'])
        return redirect(url_for('index'))
