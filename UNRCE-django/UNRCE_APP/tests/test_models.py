from django.test import TestCase
from UNRCE_APP.models import *

class TestAffiliation(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="JohnD0e", email="john.d@example.com", password="1 of THE passwords of all time")
        self.hub = RCEHub.objects.create(hub_name="Perth Hub", contact_info="No.")
        self.org = Organisation.objects.create(hub=self.hub, org_name="Royal Society for the Promotion of Cruelty to Animals", address="17 Cherry Tree Lane, The 9th Circle of Hell, Perth, Scotland")

    def test_creation(self):
        aff = Affiliation.objects.create(user= self.user, org=self.org)
        self.assertIsInstance(aff, Affiliation)