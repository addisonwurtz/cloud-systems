import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import redirect, request, url_for, render_template, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
import gbmodel
from oauth_config import client_id, authorization_base_url, redirect_callback

class Tasks(MethodView):
    def get(self):
        """
        Gets users tasks
        :return: List of dicts containing task data
        """
        if 'oauth_token' in session:
            google = OAuth2Session(client_id, token=session['oauth_token'])
            userinfo = google.get('https://tasks.googleapis.com/oauth2/v3/userinfo').json()
            model = gbmodel.get_model()
            contacts = [dict(first_name=row[0], last_name=row[1], orbit=row[2], contact_history= row[3], date_added=row[4] ) for row in model.select()]
            return render_template('view_tasks.html', tasks=tasks)        
        else:
        # Redirect to the identity provider and ask the identity provider to return the client
        #   back to /callback route with the code
            google = OAuth2Session(client_id,
                    redirect_uri = redirect_callback,
                    scope = 'https://www.googleapis.com/auth/userinfo.email ' +                   
                            'https://www.googleapis.com/auth/userinfo.profile'
            )
            authorization_url, state = google.authorization_url(authorization_base_url, prompt='login')

            # Identity provider returns URL and random "state" that must be echoed later
            #   to prevent CSRF.
            session['oauth_state'] = state
            return redirect(authorization_url)

        


