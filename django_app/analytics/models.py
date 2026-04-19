from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)

class Student(models.Model):
    name = models.CharField(max_length=255)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)
    class Meta:
        db_table="attendance"

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    class Meta:
        db_table="assignments"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table="submissions"

    