"""
Xero Payments API
"""

from .api_base import ApiBase


class Payments(ApiBase):
    """
    Class for Payments API
    """

    GET_INVOICES = '/api.xro/2.0/payments'
    GET_INVOICE_BY_ID = '/api.xro/2.0/payments/{0}'
    POST_INVOICE = '/api.xro/2.0/payments'

    def get_all(self):
        """
        Get all payments

        Returns:
            List of all payments
        """

        return self._get_request(Payments.GET_INVOICES)

    def get_by_id(self, payment_id):
        """
        Get payment by payment_id

        Parameters:
            payment_id (str): Payment ID

        Returns:
            Payment dict
        """

        return self._get_request(Payments.GET_INVOICE_BY_ID.format(payment_id))

    def post(self, data):
        """
        Create new payment

        Parameters:
            data (dict): Data to create payment

        Returns:
             Response from API
        """

        return self._update_request(data, Payments.POST_INVOICE)
