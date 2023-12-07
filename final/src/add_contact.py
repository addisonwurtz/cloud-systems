from flask import redirect, request, url_for, render_template, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
import gbmodel
from oauth_config import client_id, authorization_base_url, redirect_callback
from task_management import get_task_json

class Add(MethodView):
    def get(self):
        # If client has an OAuth2 token, use it to get their information and render
        #   the signing page with it
        if 'oauth_token' in session:
            google = OAuth2Session(client_id, token=session['oauth_token'])
            userinfo = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
            return render_template('add_contact.html', name=userinfo['name'], email=userinfo['email'],
                                   picture=userinfo['picture'])
        else:
            # Redirect to the identity provider and ask the identity provider to return the client
            #   back to /callback route with the code
            google = OAuth2Session(client_id,
                                   redirect_uri=redirect_callback,
                                   scope='https://www.googleapis.com/auth/userinfo.email ' +
                                         'https://www.googleapis.com/auth/userinfo.profile ' +
                                         'https://www.googleapis.com/auth/tasks'
                                   )
            authorization_url, state = google.authorization_url(authorization_base_url, prompt='login')

            # Identity provider returns URL and random "state" that must be echoed later
            #   to prevent CSRF.
            session['oauth_state'] = state
            return redirect(authorization_url)

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        if 'oauth_token' in session:
            # Insert based on form fields only if an OAuth2 token is present to ensure
            #   values in all fields exist

            # get database info
            model = gbmodel.get_model()
            contacts = [
                dict(user_email=row[0], first_name=row[1], last_name=row[2], orbit=row[3], contact_history=row[4]) for
                row in model.select()]
            # Get user info
            google = OAuth2Session(client_id, token=session['oauth_token'])
            userinfo = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()

            # Check if contact is already in database
            for contact in contacts:
                if userinfo["email"] == contact["user_email"] and request.form['first_name'] == contact[
                    'first_name'] and request.form['last_name'] == contact['last_name']:
                    # TODO update task/contact?
                    return redirect(url_for('view_contacts'))

            # Add new contact to database
            contact_history = []
            model.insert(userinfo["email"], request.form['first_name'], request.form['last_name'],
                         request.form['orbit'], contact_history)

            # Check for Orbits task list, create if necessary
            tasklists = google.get('https://tasks.googleapis.com/tasks/v1/users/@me/lists').json()

            # Get list of tasklists from response object
            items = tasklists['items']
            orbits_list = None

            # Check for Orbits Task list
            for tasklist in items:
                if "Orbits" == tasklist['title']:
                    orbits_list = tasklist
            # Create new list if orbits does not exist
            if orbits_list is None:
                tasklist = {"title": "Orbits"}
                orbits_list = google.post('https://tasks.googleapis.com/tasks/v1/users/@me/lists', json=tasklist).json()

            task_info = get_task_json(request.form["first_name"], request.form["last_name"], request.form['orbit'])
            task = google.post(f'https://tasks.googleapis.com/tasks/v1/lists/{orbits_list["id"]}/tasks', json=task_info)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('add_contact'))
