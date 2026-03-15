from django.shortcuts import render
from .models import Student, Attendance
from .face_engine import start_camera


def dashboard(request):

    return render(request, "dashboard.html")


def view_students(request):

    students = Student.objects.all()

    return render(request, "students.html", {"students": students})


def view_attendance(request):

    attendance = Attendance.objects.all()

    return render(request, "attendance.html", {"attendance": attendance})


def mark_attendance(request):

    if request.method == "POST":

        subject = request.POST.get("subject")

        start_camera(subject)

    return render(request, "mark.html")