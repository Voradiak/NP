from django.test import TestCase, Client
from django.urls import reverse
from hello.models import User, Course, Lesson, Test

class CreateTestFeatureTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='teacher1', password='pass', role=User.TEACHER)
        self.student = User.objects.create_user(username='student1', password='pass', role=User.STUDENT)
        self.course = Course.objects.create(title='Test Course', description='Desc', max_students=10, teacher=self.teacher)
        self.lesson = Lesson.objects.create(title='Lesson 1', content='Content', order=1, course=self.course)

    def test_create_test_button_visible_to_teacher(self):
        self.client.login(username='teacher1', password='pass')
        response = self.client.get(reverse('course_detail', args=[self.course.id]))
        self.assertContains(response, 'Создать тест')

    def test_create_test_button_not_visible_to_student(self):
        self.client.login(username='student1', password='pass')
        response = self.client.get(reverse('course_detail', args=[self.course.id]))
        self.assertNotContains(response, 'Создать тест')

    def test_create_test_view_accessible_to_teacher(self):
        self.client.login(username='teacher1', password='pass')
        response = self.client.get(reverse('create_test', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Создать тест')

    def test_create_test_view_forbidden_to_student(self):
        self.client.login(username='student1', password='pass')
        response = self.client.get(reverse('create_test', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 403)

    def test_create_test_success(self):
        self.client.login(username='teacher1', password='pass')
        response = self.client.post(reverse('create_test', args=[self.lesson.id]), {'title': 'New Test'})
        self.assertRedirects(response, reverse('course_detail', args=[self.course.id]))
        test = Test.objects.filter(title='New Test', lesson=self.lesson).first()
        self.assertIsNotNone(test)
