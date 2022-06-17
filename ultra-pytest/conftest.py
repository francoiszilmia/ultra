import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def setup(request):
    print("initiating chrome driver")
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    request.cls.driver = driver

    yield driver
    driver.close()


def pytest_addoption(parser):
    parser.addoption('--url', action='store', default=None)
    parser.addoption('--username', action='store', default = None)
    parser.addoption('--password', action='store', default = None)\

@pytest.fixture
def supply_url():
    return "https://www.saucedemo.com/"


@pytest.fixture
def credentials(request):
    # admin password123
    username = request.config.getoption('username')
    password = request.config.getoption('password')
    return {'username': username or 'standard_user', 'password': password or 'secret_sauce'}