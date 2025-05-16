from django.urls import path
from hello import views
from hello.models import LogMessage

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="hello/home.html",
)

from django.urls import path
from django.contrib.auth import views as auth_views
from hello import views
from hello.models import LogMessage

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="hello/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("about/", views.about, name="about"),
    path("log/", views.log_message, name="log"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:course_id>/enroll/", views.enroll_course, name="enroll_course"),
    path("profile/", views.profile, name="profile"),
    path("teacher/courses/", views.teacher_courses, name="teacher_courses"),
    path("teacher/courses/create/", views.create_course, name="create_course"),
    path("courses/<int:course_id>/lessons/create/", views.create_lesson, name="create_lesson"),
    path("courses/<int:course_id>/", views.course_detail, name="course_detail"),
    path("lessons/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("lessons/<int:lesson_id>/tests/create/", views.create_test, name="create_test"),
]

