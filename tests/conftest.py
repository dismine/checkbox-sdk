import pytest

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


@pytest.fixture
def login(request):
    return request.config.getoption("--login")


@pytest.fixture
def pincode(request):
    return request.config.getoption("--pincode")


@pytest.fixture
def license_key(request):
    return request.config.getoption("--license_key")
