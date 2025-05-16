from django.core.management.base import BaseCommand
from hello.models import User
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Create an admin user with role=admin, is_staff=True, and is_superuser=True'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the admin user')
        parser.add_argument('email', type=str, help='Email address for the admin user')
        parser.add_argument('password', type=str, help='Password for the admin user')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.ERROR(f'User with username "{username}" already exists.'))
        except ObjectDoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=User.ADMIN,
                is_staff=True,
                is_superuser=True
            )
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created successfully.'))
