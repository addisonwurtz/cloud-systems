from datetime import datetime
from google.cloud import datastore
from .Model import Model

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [ quote, attribution, rating, date_added ]
    where name, email, and message are Python strings
    and where date is a Python datetime
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['quote'], entity['attribution'], entity['rating'], entity['date_added']]


class model(Model):
    def __init__(self):
        self.client = datastore.Client('cloud-wurtz-awurtz')


    def select(self):
        """
        Gets all entries from the database
        Each entry contains: quote, attribution, rating, date_added
        :return: List of lists containing all rows of database
        """
        query = self.client.query(kind = 'Quote')
        entities = list(map(from_datastore,query.fetch()))
        return entities

    def insert(self, quote, attribution, rating):
        """
        Inserts entry into database
        :param quote: String
        :param attribution: String
        :param rating: float
        :return: True
        """
        key = self.client.key('Quote')
        entry = datastore.Entity(key)
        entry.update( {
            'quote': quote,
            'attribution': attribution,
            'rating': rating,
            'date_added': datetime.today(),
            })
        self.client.put(entry)
        return True

   