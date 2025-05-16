import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from hello.models import Course, Enrollment

User = get_user_model()

@pytest.mark.django_db
def test_user_registration(client):
    url = reverse('register')
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'role': User.STUDENT,
        'password1': 'complexpassword123',
        'password2': 'complexpassword123',
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after registration
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_user_login(client, django_user_model):
    user = django_user_model.objects.create_user(username='loginuser', password='password123')
    url = reverse('login')
    response = client.post(url, {'username': 'loginuser', 'password': 'password123'})
    assert response.status_code == 302  # Redirect after login

@pytest.mark.django_db
def test_course_list_view(client, django_user_model):
    user = django_user_model.objects.create_user(username='student', password='password123')
    client.login(username='student', password='password123')
    url = reverse('course_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_enroll_course(client, django_user_model):
    teacher = django_user_model.objects.create_user(username='teacher', password='password123', role=User.TEACHER)
    student = django_user_model.objects.create_user(username='student', password='password123', role=User.STUDENT)
    course = Course.objects.create(title='Test Course', description='Desc', teacher=teacher, max_students=1)
    client.login(username='student', password='password123')
    url = reverse('enroll_course', args=[course.id])
    response = client.post(url)
    # Enrollment view redirects on success
    assert response.status_code in (200, 302)
    # Enroll again to test duplicate enrollment
    response2 = client.post(url)
    assert response2.status_code == 200 or response2.status_code == 403 or b"Already enrolled" in response2.content

@pytest.mark.django_db
def test_profile_view(client, django_user_model):
    student = django_user_model.objects.create_user(username='student', password='password123', role=User.STUDENT)
    client.login(username='student', password='password123')
    url = reverse('profile')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_teacher_courses_view(client, django_user_model):
    teacher = django_user_model.objects.create_user(username='teacher', password='password123', role=User.TEACHER)
    client.login(username='teacher', password='password123')
    url = reverse('teacher_courses')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_teacher_courses_unauthorized(client, django_user_model):
    student = django_user_model.objects.create_user(username='student', password='password123', role=User.STUDENT)
    client.login(username='student', password='password123')
    url = reverse('teacher_courses')
    response = client.get(url)
    assert response.status_code == 403
