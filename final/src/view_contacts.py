from flask import redirect, request, url_for, render_template, session
from requests_oauthlib import OAuth2Session
from flask import render_template
from flask.views import MethodView
import gbmodel
from oauth_config import client_id, authorization_base_url, redirect_callback
import json
from task_management import get_task_json


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
            contacts = [
                dict(user_email=row[0], first_name=row[1], last_name=row[2], orbit=row[3], contact_history=row[4],
                     date_added=row[5]) for row in model.select() if row[0] == userinfo['email']]

            # compare contacts lists to orbits task list
            self.update_contacts(contacts, google)

            return render_template('view_contacts.html', contacts=contacts, name=userinfo['name'],
                                   email=userinfo['email'], picture=userinfo['picture'])
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

    def update_contacts(self, contacts, google):
        # Compare contacts to active tasks and create new task for each contact that does not have one
        # Get "Orbits" list id
        tasklists = google.get('https://tasks.googleapis.com/tasks/v1/users/@me/lists').json()
        items = tasklists['items']
        orbits_list = None
        # Check for Orbits Task list
        for list in items:
            if "Orbits" == list['title']:
                orbits_list = list
        # if Orbits list does not exist, create it and add task for each contact
        if orbits_list is None:
            pass
        # Otherwise update contact history for each completed task and create new task
        else:
            tasks = google.get(
                f'https://tasks.googleapis.com/tasks/v1/lists/{orbits_list["id"]}/tasks?showCompleted=true&showHidden=true').json()
            for contact in contacts:
                in_progress = False
                for task in tasks["items"]:
                    # match found
                    if str(contact["first_name"] + ' ' + contact["last_name"]) == task["title"]:
                        # if completed update contact history
                        if task["status"] != "completed":
                            in_progress = True
                if in_progress is False:
                    task_info = get_task_json(contact["first_name"], contact["last_name"], contact["orbit"])
                    google.post(f'https://tasks.googleapis.com/tasks/v1/lists/{orbits_list["id"]}/tasks', json=task_info)