from django.test import TestCase, Client
from django.contrib.auth.models import User
from login.forms import *


# Create your tests here
class RegistrationTestCase(TestCase):

    def testRedirect(self):
        # calls redirect url
        response = Client().post('/accounts/login')
        self.assertEqual(response.status_code, 301)
        
	
    def testActivePage(self):
        response = self.client.get('/accounts/login', follow=True)
        self.assertEqual(response.status_code, 200, "login page not working")

