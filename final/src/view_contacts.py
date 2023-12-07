from flask import redirect, request, url_for, render_template, session
from requests_oauthlib import OAuth2Session
from flask import render_template
from flask.views import MethodView
import gbmodel
from tasks import Tasks
from oauth_config import client_id, authorization_base_url, redirect_callback

class ViewContacts(MethodView):
    def get(self):
        """
        Retrieves all contact entries from database
        :return: List of dicts containing contact data
        """
        if 'oauth_token' in session:
            google = OAuth2Session(client_id, token=session['oauth_token'])
            userinfo = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
            model = gbmodel.get_model()
            # make list of dictionaries containing only contacts that belong to authorized user
            contacts = [dict(user_email=row[0], first_name=row[1], last_name=row[2], orbit=row[3], contact_history=row[4], date_added=row[5]) for row in model.select() if row[0] == userinfo['email']]
            
            # TODO compare contacts to active tasks and create new task for each contact that does not have one
            
            return render_template('view_contacts.html', contacts=contacts, name=userinfo['name'], email=userinfo['email'], picture=userinfo['picture'])
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
