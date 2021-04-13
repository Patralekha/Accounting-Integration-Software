import json
from os import path
from unittest.mock import Mock

from xerosdk import XeroSDK


def get_mock_xero_dict(filename):
    basepath = path.dirname(__file__)
    filepath = path.join(basepath, filename)
    mock_xero_json = open(filepath, 'r').read()
    mock_xero_dict = json.loads(mock_xero_json)
    return mock_xero_dict


def get_mock_xero_from_file(filename):
    mock_xero_dict = get_mock_xero_dict(filename)
    mock_xero = Mock()
    mock_xero.Invoices.get_all.return_value = mock_xero_dict["invoices"]
    mock_xero.Accounts.get_all.return_value = mock_xero_dict["accounts"]
    mock_xero.Contacts.get_all.return_value = mock_xero_dict["contacts"]
    mock_xero.TrackingCategories.get_all.return_value = mock_xero_dict["tracking_categories"]
    return mock_xero


def get_mock_xero():
    return get_mock_xero_from_file('mock_xero.json')


def compare_dict_keys(dict1, dict2):
    """
    Compare dict1 keys with dict2 keys and see
    if dict1 has extra keys compared to dict2

    Parameters:
        dict1 (dict): response dict from API
        dict2 (dict): mock dict

    Returns:
        Set of keys
    """
    return dict1.keys() - dict2.keys()


def xero_connect():
    """
    Xero SDK connector

    Returns:
        XeroSDK class instance
    """
    file = open('test_credentials.json', 'r')
    xero_config = json.load(file)

    connection = XeroSDK(
        base_url=xero_config['base_url'],
        client_id=xero_config['client_id'],
        client_secret=xero_config['client_secret'],
        refresh_token=xero_config['refresh_token']
    )

    return connection
