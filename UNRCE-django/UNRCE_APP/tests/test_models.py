from django.test import TestCase
from UNRCE_APP.models import *
from django.contrib.auth import get_user_model 

User = get_user_model()

class TestFollow(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="john.d@example.com", password="1 of THE passwords of all time")
        self.hub = RCEHub.objects.create(hub_name="Perth Hub", contact_info="No.")
        self.org = Organisation.objects.create(hub=self.hub, org_name="Royal Society for the Promotion of Cruelty to Animals", address="17 Cherry Tree Lane, The 9th Circle of Hell, Perth, Scotland")
        self.project = Project.objects.create(title="Seal Clubbing")
        self.project.contributing_organizations.add(self.org)

    def test_creation(self):
        fol = Follow.objects.create(following_user= self.user, followed_project=self.project)
        self.assertIsInstance(fol, Follow)
        self.assertEqual(fol.following_user, self.user)
        self.assertEqual(fol.followed_project, self.project)