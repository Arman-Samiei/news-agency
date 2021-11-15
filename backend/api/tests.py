import json
from django.contrib.auth.models import User
from django.test import TestCase, Client



# Create your tests here.
from api.models import ConfirmationCode

email = 'samiei.arman@gmail.com'

class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=email, email=email, password='1')

    def test_login(self):
        data = json.dumps({'email': email, 'password': '1'})
        response = self.client.post('/api/users/login', data, content_type="application/json")
        self.assertEquals(200, response.status_code)
        data = json.dumps({'email': 'samiei.arman@yahoo.com', 'password': '2'})
        response = self.client.post('/api/users/login', data, content_type="application/json")
        self.assertEquals(403, response.status_code)

class TestSignup(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_confirmation_codes(self):
        data = {'email': email}
        self.client.post('/api/users/confirmationcode', data, content_type='application/json')
        self.assertNotEquals(len(ConfirmationCode.objects.all()), 0)

    def test_check_confirmation_code(self):
        self.test_get_confirmation_codes()
        data = {'confirmationcode': ConfirmationCode.objects.all()[0].code, 'email': email}
        response = self.client.post('/api/users/checkconfirmationcode', data, content_type='application/json')
        self.assertEquals(200, response.status_code)
        data = {'confirmationcode': ConfirmationCode.objects.all()[0].code + 'wrong_phrase', 'email': email}
        response = self.client.post('/api/users/checkconfirmationcode', data, content_type='application/json')
        self.assertEquals(403, response.status_code)

    def test_set_password(self):
        User.objects.all().delete()
        self.test_get_confirmation_codes()
        data = {'confirmationcode': ConfirmationCode.objects.all()[0].code, 'email': email}
        self.client.post('/api/users/checkconfirmationcode', data, content_type='application/json')
        data = {'email': email, 'password': '1'}
        self.client.post('/api/users/setpassword', data, content_type='application/json')
        users = User.objects.filter(email=email)
        self.assertEquals(len(users), 1)
        data = {'email': 'samiei.arman@yahoo.com', 'password': '1'}
        response = self.client.post('/api/users/setpassword', data, content_type='application/json')
        self.assertEquals(response.status_code, 400)

