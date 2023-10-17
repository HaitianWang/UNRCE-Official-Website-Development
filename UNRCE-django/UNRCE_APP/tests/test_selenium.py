from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from captcha.models import CaptchaStore
from UNRCE_APP.models import CustomUser
#from selenium.webdriver.support.relative_locator import locate_with
from time import sleep
from django.test import tag

@tag("selenium")
class TestSignUp(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.accept_insecure_certs = True
        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.set_page_load_timeout(30)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.find_element(By.CLASS_NAME, "footer-image")
        cls.selenium.quit()
        super().tearDownClass()
        

    def tearDown(self):
        self.selenium.delete_all_cookies()
    
    def test_signup_page(self):
        self.selenium.get(self.live_server_url)
        signup = self.selenium.find_element(By.PARTIAL_LINK_TEXT,"Sign")
        signup.click()
        self.assertEqual(self.selenium.current_url, f"{self.live_server_url}/signup/")
        self.selenium.find_element(By.ID,"id_email").send_keys("JohnDoe@gmail.com")
        self.selenium.find_element(By.ID, "id_password1").send_keys("Is this a good password?")
        self.selenium.find_element(By.ID, "id_password2").send_keys("Is this a good password?")
        
        captchaID = self.selenium.find_element(By.NAME, "captcha_1").get_attribute("value")
        captchaQuery = CaptchaStore.objects.filter(hashkey=captchaID)
        self.assertTrue(captchaQuery.exists())
        self.assertEqual(captchaQuery.count(), 1)
        answer = captchaQuery.first().response
        
        self.selenium.find_element(By.NAME,"captcha_0").send_keys(answer)
        self.selenium.find_element(By.CLASS_NAME,"submit-button").click()
        self.assertEquals(self.selenium.current_url, f"{self.live_server_url}/")

        self.assertTrue(CustomUser.objects.filter(email="JohnDoe@gmail.com").exists())

    def test_login_page(self):
        john = CustomUser.objects.create(email="JohnDoe@gmail.com")
        john.set_password("Is this a good password?")
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.PARTIAL_LINK_TEXT, "Log").click()
        self.assertEqual(self.selenium.current_url, f"{self.live_server_url}/login/")
        self.selenium.find_element(By.ID,"id_username").send_keys("JohnDoe@gmail.com")
        self.selenium.find_element(By.ID, "id_password").send_keys("Is this a good password?")
        
        captchaID = self.selenium.find_element(By.NAME, "captcha_1").get_attribute("value")
        captchaQuery = CaptchaStore.objects.filter(hashkey=captchaID)
        self.assertTrue(captchaQuery.exists())
        self.assertEqual(captchaQuery.count(), 1)
        answer = captchaQuery.first().response

        self.selenium.find_element(By.NAME,"captcha_0").send_keys(answer)
        sleep(3)
        self.selenium.find_element(By.CLASS_NAME,"submit-button").click()
        sleep(3)
        self.assertEquals(self.selenium.current_url, f"{self.live_server_url}/")

        account_links = self.selenium.find_elements(By.PARTIAL_LINK_TEXT,"Account").count()
        self.assertGreater(account_links,0)

