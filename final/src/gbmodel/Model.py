class Model():
    def select(self):
        """
        Gets all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def insert(self, first_name, last_name, orbit, contact_history=[]):
        """
        Inserts entry into database
        :param first_name: String
        :param last_name: String
        :param orbit: String
        :param contact_history: list
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass
