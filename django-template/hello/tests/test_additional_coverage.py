import pytest
from django.urls import reverse
from django.core.management import call_command
from django.contrib.auth import get_user_model
from hello.models import Course, Lesson, Test

User = get_user_model()

@pytest.mark.django_db
def test_create_course_view(client):
    teacher = User.objects.create_user(username='teacher', password='pass', role=User.TEACHER)
    client.login(username='teacher', password='pass')
    url = reverse('create_course')
    data = {'title': 'New Course', 'description': 'Desc', 'max_students': 10}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Course.objects.filter(title='New Course').exists()

@pytest.mark.django_db
def test_create_lesson_view(client):
    teacher = User.objects.create_user(username='teacher', password='pass', role=User.TEACHER)
    course = Course.objects.create(title='Course1', description='Desc', teacher=teacher)
    client.login(username='teacher', password='pass')
    url = reverse('create_lesson', args=[course.id])
    data = {'title': 'Lesson1', 'content': 'Content', 'order': 1}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Lesson.objects.filter(title='Lesson1', course=course).exists()

@pytest.mark.django_db
def test_lesson_detail_view(client):
    teacher = User.objects.create_user(username='teacher', password='pass', role=User.TEACHER)
    course = Course.objects.create(title='Course1', description='Desc', teacher=teacher)
    lesson = Lesson.objects.create(title='Lesson1', content='Content', order=1, course=course)
    client.login(username='teacher', password='pass')
    url = reverse('lesson_detail', args=[lesson.id])
    response = client.get(url)
    assert response.status_code == 200
    assert b'Lesson1' in response.content

@pytest.mark.django_db
def test_create_test_view(client):
    teacher = User.objects.create_user(username='teacher', password='pass', role=User.TEACHER)
    course = Course.objects.create(title='Course1', description='Desc', teacher=teacher)
    lesson = Lesson.objects.create(title='Lesson1', content='Content', order=1, course=course)
    client.login(username='teacher', password='pass')
    url = reverse('create_test', args=[lesson.id])
    data = {'title': 'Test1'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Test.objects.filter(title='Test1', lesson=lesson).exists()

@pytest.mark.django_db
def test_createadmin_command():
    out = []
    call_command('createadmin', username='adminuser', password='adminpass', role='admin', stdout=out.append)
    from hello.models import User
    admin = User.objects.filter(username='adminuser').first()
    assert admin is not None
    assert admin.is_superuser
    assert admin.is_staff
    assert admin.role == 'admin'
