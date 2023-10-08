from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium import webdriver

class TestSignUp(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(15)
        cls.selenium.set_page_load_timeout(15)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_signup_page(self):
        return
        self.selenium.get(self.live_server_url)
        signup = self.selenium.find_element(By.PARTIAL_LINK_TEXT,"Sign")
        signup.click()
        self.assertEqual(self.selenium.current_url, (self.live_server_url + "/signup/"))
        #email = self.selenium.find_element(By.ID, "id_email")
        #email.send_keys("JohnDoe@gmail.com")



