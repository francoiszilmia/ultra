import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from Screenshot import Screenshot_Clipping
import json
import logging
import allure

logging.basicConfig(
    level=logging.INFO,
)
create_ultra_logger = logging.getLogger(__name__)


@allure.story('Logon https://www.saucedemo.com website')
@pytest.mark.usefixtures("setup")
class TestLogon:
    with allure.step('Open config setting'):
        with open('data/pages_conf.json', 'r') as f:
            search_page_conf = json.load(f)["search"]

    @allure.step('Logon www.saucedemo.com ')
    def test_logon(self, pytestconfig):
        with allure.step('Check homepage title'):
            username: str = pytestconfig.getoption('username')
            password: str = pytestconfig.getoption('password')
            create_ultra_logger.info(f'Retrieved username = {username}')
            create_ultra_logger.info(f'Retrieved password = {password}')

            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located(
                (self.search_page_conf["Username"]["by"], self.search_page_conf["Username"]["value"])))
            wait.until(EC.presence_of_element_located(
                (self.search_page_conf["Password"]["by"], self.search_page_conf["Password"]["value"])))
            self.driver.find_element(by=self.search_page_conf["Username"]["by"],
                                     value=self.search_page_conf["Username"]["value"]).send_keys(username)
            self.driver.find_element(by=self.search_page_conf["Password"]["by"],
                                     value=self.search_page_conf["Password"]["value"]).send_keys(password)
            self.driver.find_element(by=self.search_page_conf["Login"]["by"],
                                     value=self.search_page_conf["Login"]["value"]).click()

            title = self.driver.title
            create_ultra_logger.info(f'saucedemo titile = {title}')
            assert "Swag Labs" in title, 'Homepage title is not correct!'

    @allure.step('Add item to cart')
    def test_add_cart(self):
        with allure.step('Add first item to cart'):
            wait = WebDriverWait(self.driver, 10)
            create_ultra_logger.info(
                f'Add to cart button = {self.search_page_conf["add_cart"]["value"]}')
            wait.until(EC.presence_of_element_located(
                (self.search_page_conf["add_cart"]["by"], self.search_page_conf["add_cart"]["value"])))
            sleep(2)
            cart = self.driver.find_element(by=self.search_page_conf["add_cart"]["by"],
                                            value=self.search_page_conf["add_cart"]["value"])
            self.driver.find_element(by=self.search_page_conf["add_cart"]["by"],
                                     value=self.search_page_conf["add_cart"]["value"]).click()
            sleep(2)
            assert cart, 'Cannot add item to cart!'

    @allure.step('Checkout item')
    def test_checkout_cart(self):
        with allure.step('Checkout item'):
            wait = WebDriverWait(self.driver, 10)
            create_ultra_logger.info(
                f'Checkout button = {self.search_page_conf["shopping_cart_badge"]["value"]}')

            wait.until(EC.presence_of_element_located(
                (self.search_page_conf["shopping_cart_badge"]["by"],
                 self.search_page_conf["shopping_cart_badge"]["value"])))
            self.driver.find_element(by=self.search_page_conf["shopping_cart_badge"]["by"],
                                     value=self.search_page_conf["shopping_cart_badge"]["value"]).click()
            sleep(1)

            wait.until(EC.presence_of_element_located(
                (self.search_page_conf["checkout"]["by"],
                 self.search_page_conf["checkout"]["value"])))

            self.driver.find_element(by=self.search_page_conf["checkout"]["by"],
                                     value=self.search_page_conf["checkout"]["value"]).click()
            sleep(1)

            wait.until(EC.presence_of_element_located(
                (self.search_page_conf["firstName"]["by"],
                 self.search_page_conf["firstName"]["value"])))

            wait.until(EC.presence_of_element_located(
                (self.search_page_conf["lastName"]["by"],
                 self.search_page_conf["lastName"]["value"])))

            with allure.step('Checkout your information'):
                with open('data/booking.json', 'r') as f:
                    body = json.load(f)
                    firstname = body['firstname']
                    lastname = body['lastname']
                    postalcode = body['postalCode']

                    create_ultra_logger.info(f'Retrieved firstname = {firstname}')
                    create_ultra_logger.info(f'Retrieved lastname = {lastname}')
                    create_ultra_logger.info(f'Retrieved zipcode = {postalcode}')

                    self.driver.find_element(by=self.search_page_conf["firstName"]["by"],
                                             value=self.search_page_conf["firstName"]["value"]).send_keys(firstname)
                    self.driver.find_element(by=self.search_page_conf["lastName"]["by"],
                                             value=self.search_page_conf["lastName"]["value"]).send_keys(lastname)
                    self.driver.find_element(by=self.search_page_conf["postalCode"]["by"],
                                             value=self.search_page_conf["postalCode"]["value"]).send_keys(postalcode)
                    sleep(1)

                    wait.until(EC.presence_of_element_located(
                        (self.search_page_conf["continue"]["by"],
                         self.search_page_conf["continue"]["value"])))

                    wait.until(EC.presence_of_element_located(
                        (self.search_page_conf["continue"]["by"],
                         self.search_page_conf["continue"]["value"]))).click()
                    sleep(2)

                    wait.until(EC.presence_of_element_located(
                        (self.search_page_conf["finish"]["by"],
                         self.search_page_conf["finish"]["value"])))

                    wait.until(EC.presence_of_element_located(
                        (self.search_page_conf["finish"]["by"],
                         self.search_page_conf["finish"]["value"]))).click()

                    res = wait.until(EC.presence_of_element_located(
                        (self.search_page_conf["order"]["by"],
                         self.search_page_conf["order"]["value"])))
                    assert res, f'Order uncompleted!'

                    img = wait.until(EC.presence_of_element_located(
                        (self.search_page_conf["pony_express"]["by"],
                         self.search_page_conf["pony_express"]["value"])))
                    assert img, f'Pony express image not displaying!'

                    sleep(2)

    @allure.step('Make order screenshot')
    def test_order_screenshot(self):
        with allure.step('Order screenshot'):
            # set default driver to desktop size and take screenshot
            ob = Screenshot_Clipping.Screenshot()
            self.driver.maximize_window()
            ob.full_Screenshot(self.driver, save_path=r'.', image_name='screenshots/my-order.png')
