from django.db import models
from django.contrib.auth.models import AbstractUser


class Fields(models.Model):
    FIELDS_CHOICES = (
        ('Programming', 'Programming'),
        ('Tailoring', 'Tailoring'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Other', 'Other')
    )
    name = models.CharField(max_length=255, choices=FIELDS_CHOICES, null=False, blank=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Company'),
        (2, 'Person'),
        (3, 'Admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, blank=False, null=False, default=3)


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    creation_year = models.IntegerField(blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    number = models.CharField(max_length=11, blank=False, null=False)
    fields = models.ManyToManyField(Fields, blank=True)


class PersonProfile(models.Model):
    SEX_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    age = models.PositiveIntegerField(blank=False, null=False)
    resume = models.FileField(upload_to='Resumes/', blank=True, null=True)
    fields = models.ManyToManyField(Fields, blank=True)



