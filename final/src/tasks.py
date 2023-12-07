import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import redirect, request, url_for, render_template, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
import gbmodel
from oauth_config import client_id, authorization_base_url, redirect_callback

class Tasks(MethodView):
    def get(self):
        """Shows basic usage of the Tasks API.
        Prints the title and ID of the first 10 task lists.
        """
        # If client has an OAuth2 token, use it to get their information and render
        #   the signing page with it
        if 'oauth_token' in session:
            google = OAuth2Session(client_id, token=session['oauth_token'])
            tasklists = google.get('https://tasks.googleapis.com/tasks/v1/users/@me/lists').json()
            # Get list of tasklists from response object
            items = tasklists['items']
            orbits_list = None
            # Check for Orbits Task list
            for list in items:
                if "Orbits" == list['title']:
                    orbits_list = list
            if orbits_list is None:
                list = {"title": "Orbits"}
                orbits_list = google.post('https://tasks.googleapis.com/tasks/v1/users/@me/lists', json=list).json()

            # Get tasks from Orbits list
            list_id = orbits_list["id"]
            tasks = google.get(f'https://tasks.googleapis.com/tasks/v1/lists/{list_id}/tasks?showCompleted=true&showHidden=true').json()
            
            return render_template('view_tasks.html', tasks=tasks["items"], tasklist=str(orbits_list))
        else:
        # Redirect to the identity provider and ask the identity provider to return the client
        #   back to /callback route with the code
            google = OAuth2Session(client_id,
                    redirect_uri = redirect_callback,
                    scope = 'https://www.googleapis.com/auth/userinfo.email ' +                   
                            'https://www.googleapis.com/auth/userinfo.profile ' +
                            'https://www.googleapis.com/auth/tasks'
                            #'https://www.googleapis.com/auth/generative-language'
            )
            authorization_url, state = google.authorization_url(authorization_base_url, prompt='login')

            # Identity provider returns URL and random "state" that must be echoed later
            #   to prevent CSRF.
            session['oauth_state'] = state
            return redirect(authorization_url)
