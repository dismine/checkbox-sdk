import pytest

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.storage.simple import SessionStorage


# This code is used to facilitate testing by allowing dynamic input of credentials
# such as cashier's login, pin code, and cash register license key.
# Hardcoding these credentials is not an option as each user must pass their own data.
# We rely on a Checkbox instance that we do not control, and the method to obtain
# these credentials is detailed in Checkbox's documentation.
# To pass the input test data, use the following command:
# pytest --login=<login> --pincode=<pin code> --license_key=<key>
# in case of tox
# tox -- --login=<login> --pincode=<pin code> --license_key=<key>


def pytest_addoption(parser):
    parser.addoption("--login", action="store", help="Cashier's login")
    parser.addoption("--pincode", action="store", help="Cashier's PIN code")
    parser.addoption("--license_key", action="store", help="Cash register license key")
    # Checkbox has limitation on number of created test receipts. 100 on month. To avoid reaching this limit test this
    # part only when necessary.
    parser.addoption("--check_receipt_creation", action="store_true", default=False, help="Check receipt creation")


@pytest.fixture(scope="session")
def login(request):
    return request.config.getoption("--login")


@pytest.fixture(scope="session")
def pincode(request):
    return request.config.getoption("--pincode")


@pytest.fixture(scope="session")
def license_key(request):
    return request.config.getoption("--license_key")


@pytest.fixture(scope="session")
def auth_token(pincode, license_key):
    # Will be executed before the first test
    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.cashier.authenticate_pin_code(pin_code=pincode, license_key=license_key)
    yield storage.token
    # Will be executed after the last test
    client.cashier.sign_out(storage)
    client.close()


@pytest.fixture(scope="session")
def check_receipt_creation(request):
    return request.config.getoption("--check_receipt_creation")
