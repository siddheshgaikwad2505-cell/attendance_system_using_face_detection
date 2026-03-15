from django.db import models


class Student(models.Model):

    name = models.CharField(max_length=100)
    roll = models.CharField(max_length=20)
    image = models.ImageField(upload_to='students/')

    def __str__(self):
        return self.name


class Attendance(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"