from django.db import models
from datetime import date


class Employee(models.Model):
    code = models.CharField("Employee Code", max_length=255, unique=True)
    name = models.CharField("Employee Name", max_length=255)
    department = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def age(self):
        today = date.today()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @property
    def experience(self):
        today = date.today()
        date_of_joining = self.date_of_joining
        return today.year - date_of_joining.year - ((today.month, today.day) < (date_of_joining.month,
                                                                                date_of_joining.day))
