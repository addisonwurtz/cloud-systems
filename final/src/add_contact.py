from flask import redirect, request, url_for, render_template, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
import gbmodel
from oauth_config import client_id, authorization_base_url, redirect_callback
from datetime import date, timedelta

class Add(MethodView):
    def get(self):
        # If client has an OAuth2 token, use it to get their information and render
        #   the signing page with it
        if 'oauth_token' in session:
            google = OAuth2Session(client_id, token=session['oauth_token'])
            userinfo = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
            return render_template('add_contact.html', name=userinfo['name'], email=userinfo['email'], picture=userinfo['picture'])
        else:
        # Redirect to the identity provider and ask the identity provider to return the client
        #   back to /callback route with the code
            google = OAuth2Session(client_id,
                    redirect_uri = redirect_callback,
                    scope = 'https://www.googleapis.com/auth/userinfo.email ' +                   
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
            model = gbmodel.get_model()
            contact_history = []
            model.insert(request.form['first_name'], request.form['last_name'], request.form['orbit'], contact_history)

            # Check for Orbits task list, create if necessary
            google = OAuth2Session(client_id, token=session['oauth_token'])
            tasklists = google.get('https://tasks.googleapis.com/tasks/v1/users/@me/lists').json()
            
            # Get list of tasklists from response object
            items = tasklists['items']
            orbits_list = None
            
            # Check for Orbits Task list
            for list in items:
                if "Orbits" == list['title']:
                    orbits_list = list
            # Create new list if orbits does not exist
            if orbits_list is None:
                list = {"title": "Orbits"}
                orbits_list = google.post('https://tasks.googleapis.com/tasks/v1/users/@me/lists', json=list).json()

            # Add new task based on contact info
            # orbit = request.form['orbit']
            if orbit == "daily":
                delta = timedelta(days=1)
            elif orbit == "weekly":
                delta = timedelta(weeks=1)
            elif orbit == "monthly":
                    delta = timedelta(days=30)
            elif orbit == "quarterly":
                delta = timedelta(weeks=12)
            elif orbit == "semi_annually":
                delta = timedelta(weeks=24)
            elif orbit == "annually":
                delta = timedelta(weeks = 56)
            else:
               delta = timedelta(days=0)

            task_json = {
                "title": str(request.form['first_name']) + str(request.form['last_name']),
                "due": date.today + delta,
                "notes": "Time to say hello!"
            }
            task = google.post(f'https://tasks.googleapis.com/tasks/v1/lists/{orbits_list["id"]}/tasks', json=task_json)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('add_contact'))