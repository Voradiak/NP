from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView
from hello.forms import LogMessageForm, UserRegistrationForm, EnrollmentForm, CourseCreateForm, LessonCreateForm, TestCreateForm
from hello.models import LogMessage, Course, Enrollment, User, Lesson

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "hello/about.html")

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "hello/log_message.html", {"form": form})

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "hello/register.html", {"form": form})

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "hello/course_list.html", {"courses": courses})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment_count = Enrollment.objects.filter(course=course).count()
    if enrollment_count >= course.max_students:
        return HttpResponse("Course enrollment limit reached.", status=403)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        return redirect("course_list")
    else:
        return HttpResponse("Already enrolled in this course.")

@login_required
def profile(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, "hello/profile.html", {"enrollments": enrollments})

@login_required
def teacher_courses(request):
    if request.user.role != User.TEACHER:
        return HttpResponse("Unauthorized", status=403)
    courses = Course.objects.filter(teacher=request.user)
    return render(request, "hello/teacher_courses.html", {"courses": courses})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("home")

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request,'hello/login.html',{'form':form})

@login_required
def create_course(request):
    if request.user.role != User.TEACHER:
        return HttpResponse("Доступ запрещён", status=403)
    if request.method == "POST":
        form = CourseCreateForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect("teacher_courses")
    else:
        form = CourseCreateForm()
    return render(request, "hello/create_course.html", {"form": form})

@login_required
def create_lesson(request, course_id):
    if request.user.role != User.TEACHER:
        return HttpResponse("Доступ запрещён", status=403)
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = LessonCreateForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect("course_detail", course_id=course.id)
    else:
        form = LessonCreateForm()
    return render(request, "hello/create_lesson.html", {"form": form, "course": course})

@login_required
def create_test(request, lesson_id):
    if request.user.role != User.TEACHER:
        return HttpResponse("Доступ запрещён", status=403)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == "POST":
        form = TestCreateForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.lesson = lesson
            test.save()
            return redirect("lesson_detail", lesson_id=lesson.id)
    else:
        form = TestCreateForm()
    return render(request, "hello/create_test.html", {"form": form, "lesson": lesson})

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    tests = lesson.tests.all()
    return render(request, "hello/lesson_detail.html", {"lesson": lesson, "tests": tests})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    # Fetch tests for each lesson
    lessons_with_tests = []
    for lesson in lessons:
        tests = lesson.tests.all()
        lessons_with_tests.append({
            'lesson': lesson,
            'tests': tests
        })
    is_enrolled = Enrollment.objects.filter(course=course, student=request.user).exists()
    enrollment_count = Enrollment.objects.filter(course=course).count()
    remaining_seats = course.max_students - enrollment_count
    return render(request, "hello/course_detail.html", {
        "course": course,
        "lessons_with_tests": lessons_with_tests,
        "is_enrolled": is_enrolled,
        "remaining_seats": remaining_seats
    })
