from django.test import LiveServerTestCase
import UNRCE_APP
from selenium.webdriver.common.by import By
from selenium import webdriver

class TestLogin(LiveServerTestCase):
    pass 

class TestSignUp(LiveServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(15)
        cls.selenium.set_page_load_timeout(15)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_login(self):
        pass

    def test_bad_passwords(self):
        self.selenium.get(self.live_server_url)
        signUpButton = self.selenium.find_element(By.PARTIAL_LINK_TEXT,"Sign")
        signUpButton.click()
        self.assertEqual(self.selenium.current_url, (self.live_server_url + "/signup/"))


class TestProjectSubmission(LiveServerTestCase):
    pass

