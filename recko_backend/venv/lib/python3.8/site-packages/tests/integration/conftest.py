import pytest

from tests.common.utils import get_mock_xero, xero_connect


@pytest.fixture
def mock_xero():
    return get_mock_xero()


@pytest.fixture(scope='module')
def xero():
    return xero_connect()
