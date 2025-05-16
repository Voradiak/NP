from django.core.management import call_command
from django.test import TestCase
from hello.models import User
from io import StringIO

class CreateAdminCommandTest(TestCase):
    def test_create_admin_user_success(self):
        out = StringIO()
        call_command('createadmin', 'adminuser', 'admin@example.com', 'password123', stdout=out)
        self.assertIn('Admin user "adminuser" created successfully.', out.getvalue())
        user = User.objects.get(username='adminuser')
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertEqual(user.role, User.ADMIN)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_admin_user_already_exists(self):
        User.objects.create_user(username='adminuser', email='admin@example.com', password='password123', role=User.ADMIN, is_staff=True, is_superuser=True)
        out = StringIO()
        call_command('createadmin', 'adminuser', 'admin@example.com', 'password123', stdout=out)
        self.assertIn('User with username "adminuser" already exists.', out.getvalue())
