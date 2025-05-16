from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from hello.models import LogMessage, User, Enrollment, Course, Lesson, Test

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")

class UserLoginForm(AuthenticationForm):
    pass

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ("course",)

class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'order']
        labels = {
            'title': 'Название урока',
            'content': 'Содержание',
            'order': 'Порядок',
        }

class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title']
        labels = {
            'title': 'Название теста',
        }

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'max_students']
        labels = {
            'title': 'Название курса',
            'description': 'Описание',
            'max_students': 'Максимум студентов',
        }
