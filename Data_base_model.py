from django.db import models


class Enrollment(models.Model):
    COURSE_CHOICES = [
        ('beginner', 'Beginner (Full Course)'),
        ('refresher', 'Refresher Course'),
        ('license', 'License Processing Only'),
    ]

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    course_interest = models.CharField(max_length=20, choices=COURSE_CHOICES)
    message = models.TextField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course_interest}"