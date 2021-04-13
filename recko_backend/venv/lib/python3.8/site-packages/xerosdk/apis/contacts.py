"""
Xero Contacts API
"""

from .api_base import ApiBase


class Contacts(ApiBase):
    """
    Class for Contacts API
    """

    GET_CONTACTS = "/api.xro/2.0/contacts"
    POST_CONTACTS = "/api.xro/2.0/contacts"

    def get_all(self):
        """
        Get all contacts

        Returns:
            List of all contacts
        """

        return self._get_request(Contacts.GET_CONTACTS)

    def post(self, data):
        """
        create new contact

        Parameters:
        data (dict): Data to create contact

        Returns:
             Response from API
        """

        return self._post_request(data, Contacts.POST_CONTACTS)
