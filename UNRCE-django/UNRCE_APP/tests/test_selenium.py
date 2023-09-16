from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium import webdriver
import time  #TODO: Delete after debugging selenium problems
class TestLogin(LiveServerTestCase):
    pass 

class TestSignUp(LiveServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.selenium = webdriver.Edge()
        cls.selenium.implicitly_wait(15)
        cls.selenium.set_page_load_timeout(15)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_login(self):
        pass

    def test_bad_passwords(self):
        '''print("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        self.selenium.get(self.live_server_url)
        print("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
        signUpButton = self.selenium.find_element(By.PARTIAL_LINK_TEXT,"Sign")
        print("3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")
        signUpButton.click()
        print("444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444")
        self.assertEqual(self.selenium.current_url, (self.live_server_url + "/signup/"))
        print("5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")'''
        self.selenium.get(self.live_server_url)
        time.sleep(5)

class TestProjectSubmission(LiveServerTestCase):
    pass

