from django.test import LiveServerTestCase
import UNRCE_APP
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

class TestLogin(LiveServerTestCase):
    pass 

class TestSignUp(LiveServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_login(self):
        pass

    def test_bad_passwords(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.PARTIAL_LINK_TEXT,"Sign").click()
        self.assertEqual(self.selenium.current_url,"/signup")


class TestProjectSubmission(LiveServerTestCase):
    pass

