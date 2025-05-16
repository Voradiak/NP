from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Course, Lesson, Enrollment, Test, Question

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at', 'max_students')
    list_filter = ('teacher',)
    search_fields = ('title', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course', 'student')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson')
    list_filter = ('lesson',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'text', 'correct_choice')
    list_filter = ('test',)
