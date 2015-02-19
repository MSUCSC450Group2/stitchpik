from django.test import TestCase, Client
from django.contrib.auth.models import User
from login.forms import *


# Create your tests here
class RegistrationTestCase(TestCase):
    
    def setUp(self):
	return


    def testBadName(self):
        response = Client().post('/stitchpick/templates/login/registration/login.html')
        assert.assertEqual(response.status_code, 200)
        
	
.
