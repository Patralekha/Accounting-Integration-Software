from tests.common.utils import compare_dict_keys


def test_invoices(xero, mock_xero):
    """
    Test Xero Invoices object

    Parameters:
        xero (obj): Xero SDK instance
        mock_xero (obj): mock Xero SDK instance
    """

    invoices = xero.Invoices.get_all()["Invoices"]
    mock_invoices = mock_xero.Invoices.get_all()

    assert compare_dict_keys(invoices[0], mock_invoices[0]) == set()
    assert compare_dict_keys(mock_invoices[0], invoices[0]) == set()


def test_accounts(xero, mock_xero):
    """
    Test Xero Accounts object

    Parameters:
        xero (obj): Xero SDK instance
        mock_xero (obj): mock Xero SDK instance
    """

    accounts = xero.Accounts.get_all()["Accounts"]
    mock_accounts = mock_xero.Accounts.get_all()

    assert compare_dict_keys(accounts[0], mock_accounts[0]) == set()
    assert compare_dict_keys(mock_accounts[0], accounts[0]) == set()


def test_contacts(xero, mock_xero):
    """
    Test Xero Contacts object

    Parameters:
        xero (obj): Xero SDK instance
        mock_xero (obj): mock Xero SDK instance
    """

    contacts = xero.Contacts.get_all()["Contacts"]
    mock_contacts = mock_xero.Contacts.get_all()

    assert compare_dict_keys(contacts[0], mock_contacts[0]) == set()
    assert compare_dict_keys(mock_contacts[0], contacts[0]) == set()


def test_tracking_categories(xero, mock_xero):
    """
    Test Xero TrackingCategories object

    Parameters:
        xero (obj): Xero SDK instance
        mock_xero (obj): mock Xero SDK instance
    """

    tracking_categories = xero.TrackingCategories.get_all()["TrackingCategories"]
    mock_tracking_categories = mock_xero.TrackingCategories.get_all()

    assert compare_dict_keys(tracking_categories[0], mock_tracking_categories[0]) == set()
    assert compare_dict_keys(mock_tracking_categories[0], tracking_categories[0]) == set()
