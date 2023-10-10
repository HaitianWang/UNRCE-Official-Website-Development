from django.test import TestCase, Client
from UNRCE_APP.models import CustomUser
from captcha.models import CaptchaStore
from django.urls import reverse

class TestPages(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
    
    def get_captcha_value(self, response):
        captcha_key = response.context.get("captcha_key")
        captchaQuery = CaptchaStore.objects.filter(hashkey=captcha_key)
        self.assertTrue(captchaQuery.exists())
        self.assertEqual(captchaQuery.count(), 1)
        captcha = captchaQuery.first()
        return captcha.response, captcha_key

    def test_signup(self):
        response = self.client.get(reverse("UNRCE_APP:signup"))
        self.assertEqual(response.status_code, 200)
        captcha_value, captcha_key = self.get_captcha_value(response)
        response = self.client.post(
            reverse("UNRCE_APP:signup"),
            {
                "email":"JohnDoe@gmail.com",
                "password1":"Is this a good password?",
                "password2":"Is this a good password?",
                "captcha_0":captcha_value,
                "captcha_1":captcha_key,
            }
        )
        self.assertEqual(response.status_code, 302, "Status code doesn't indicate redirection")
        self.assertTrue(CustomUser.objects.filter(email="JohnDoe@gmail.com").exists())
        
    #def test_signup_captcha_reuse(self):
        
    def test_login(self):
        user = CustomUser.objects.create(email="JohnDoe@gmail.com")
        user.set_password("Is this a good password?")
        user.save()
        response = self.client.get(reverse("UNRCE_APP:login"))
        self.assertEqual(response.status_code, 200)
        captcha_value, captcha_key = self.get_captcha_value(response)
        response= self.client.post(
            reverse("UNRCE_APP:login"),
            {
                "username":"JohnDoe@gmail.com",
                "password":"Is this a good password?",
                "captcha_0":captcha_value,
                "captcha_1":captcha_key
            }
        )
        self.assertEqual(user, response.wsgi_request.user)