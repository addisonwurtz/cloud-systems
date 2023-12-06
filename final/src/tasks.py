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
            usertasks = google.get('https://tasks.googleapis.com/tasks/v1/users/@me/lists').json()
            tasks = str(usertasks)
            return render_template('view_tasks.html', tasks=tasks)
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
"""
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", scopes='https://www.googleapis.com/auth/tasks')
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = Flow.from_client_secrets_file(
                    'client_secrets.json', scopes=['https://www.googleapis.com/auth/tasks'])
                flow.redirect_uri = 'https://final-jpg37fqnga-uw.a.run.app/view_tasks'

                authorization_response = request.url
                flow.fetch_token(authorization_response=authorization_response)
                creds = flow.credentials
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        try:
            service = build("tasks", "v1", credentials=creds)

            # Call the Tasks API
            results = service.tasklists().list(maxResults=10).execute()
            items = results.get("items", [])

            #if not items:
            #    print("No task lists found.")
            #    return

            #print("Task lists:")
            #for item in items:
            #    print(f"{item['title']} ({item['id']})")
            #return items
            return render_template('view_tasks.html', tasks=items)
        except HttpError as err:
            print(err)
"""
