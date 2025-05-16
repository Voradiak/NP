from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Administrator'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    # Additional profile fields can be added here

class LogMessage(models.Model):
    message = models.TextField()
    log_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(default=timezone.now)
    max_students = models.PositiveIntegerField(default=30)  # configurable limit

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(default=timezone.now)
    progress = models.JSONField(default=dict)  # to track lesson completion, e.g. {lesson_id: True}

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

class Test(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Test for {self.lesson.title}"

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    choice_a = models.CharField(max_length=200)
    choice_b = models.CharField(max_length=200)
    choice_c = models.CharField(max_length=200)
    choice_d = models.CharField(max_length=200)
    correct_choice = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

    def __str__(self):
        return f"Question for {self.test.title}"
