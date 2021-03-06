from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Image
from image_manipulation.forms import *

# Create your tests here
class RegistrationTestCase(TestCase):

    def testAppRedirect(self):
        # calls redirect url
        response = Client().post('/application')
        self.assertEqual(response.status_code, 301, "urls to /application not working")
        
	
    def testActiveAppPage(self):
        response = self.client.get('/application', follow=True)
        self.assertEqual(response.status_code, 200, "application page not working")
