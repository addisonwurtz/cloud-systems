# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from google.cloud import datastore
from .Model import Model
import os

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [ user_email, first_name, last_name, orbit, contact_history, date_added ]
        where first_name, last_name, and orbit are Python strings
        where contact_history is a list of Python datetimes
        and where date_added is a Python datetime
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['user_email'], entity['first_name'], entity['last_name'], entity['orbit'], entity['contact_history'], entity['date_added']]


class model(Model):
    def __init__(self):
        self.client = datastore.Client('cloud-wurtz-awurtz')


    def select(self):
        """
        Gets all entries from the database
        Each entry contains: user_email, first_name, last_name, orbit, contact_history, and date_added
        :return: List of lists containing all rows of database
        """
        query = self.client.query(kind='Contact')
        entities = list(map(from_datastore, query.fetch()))
        return entities

    def insert(self, user_email, first_name, last_name, orbit, contact_history):
        """
        Inserts entry into database
        :param user_email: String
        :param first_name: String
        :param last_name: String
        :param orbit: String
        :param contact_history: list
        :return: True
        """
        key = self.client.key('Contact')
        entry = datastore.Entity(key)
        entry.update( {
            'user_email': user_email,
            'first_name': first_name,
            'last_name': last_name,
            'orbit': orbit,
            'contact_history': contact_history,
            'date_added': datetime.today(),
            })
        self.client.put(entry)
        return True

   