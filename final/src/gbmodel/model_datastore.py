from datetime import datetime
from google.cloud import datastore
from .Model import Model

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [ first_name, last_name, orbit, contact_history, date_added ]
        where first_name, last_name, and orbit are Python strings
        where contact_history is a list of Python datetimes
        and where date_added is a Python datetime
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['first_name'], entity['last_name'], entity['orbit'], entity['contact_history'], entity['date_added']]


class model(Model):
    def __init__(self):
        self.client = datastore.Client('cloud-wurtz-awurtz')


    def select(self):
        """
        Gets all entries from the database
        Each entry contains: quote, attribution, rating, date_added
        :return: List of lists containing all rows of database
        """
        query = self.client.query(kind='Contact')
        entities = list(map(from_datastore, query.fetch()))
        return entities

    def insert(self, first_name, last_name, orbit, contact_history):
        """
        Inserts entry into database
        :param first_name: String
        :param last_name: String
        :param orbit: String
        :param contact_history: list
        :return: True
        """
        key = self.client.key('Contact')
        entry = datastore.Entity(key)
        entry.update( {
            'first_name': first_name,
            'last_name': last_name,
            'orbit': orbit,
            'contact_history': contact_history,
            'date_added': datetime.today(),
            })
        self.client.put(entry)
        return True

   