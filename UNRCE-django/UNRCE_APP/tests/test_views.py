from django.test import LiveServerTestCase, Client

class TestPages(LiveServerTestCase):
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
    
    def test_landing_page(self):
        response = self.client.get("/")
        
        