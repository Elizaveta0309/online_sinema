from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseAdminTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.login()

    def create_user(self):
        username, password = 'admin', 'admin'
        user = User.objects.get_or_create(
            username=username,
            email='admin@test.com',
            is_superuser=True
        )[0]
        user.set_password(password)
        user.save()
        self.user = user
        return username, password

    def login(self):
        username, password = self.create_user()
        self.client.login(username=username, password=password)

class ClientAdminTestCsae(BaseAdminTestCase):

    def test_details(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_template(self):
        body = {
        'name': 'new_user',
        'description': 'text',
        'event': 'admin',
        'subject': 'new',
        'channel': 'email',
        'template': 'it is a template'
    }
        response = self.client.post('/admin/notifications/template/add/', json=body)
        assert response.status_code == HTTPStatus.OK


    def test_shedule_mail(self, template_id):
        body = {
        'name': 'new_user',
        'description': 'text',
        'user_group': 'all',
        'frequency': 'once',
        'priority': 'low',
        'template': template_id
    }
        response = self.client.put('admin/notifications/schedulemail/add/', json=body)
        assert response.status_code == HTTPStatus.OK
