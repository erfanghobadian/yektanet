from django.db import models
from User.models import CompanyProfile, PersonProfile
from User.models import Fields


class Work(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to='Work-Image/')
    expire_date = models.DateField()
    salary = models.IntegerField(default=0, blank=False, null=False)
    hours = models.IntegerField(blank=False, null=False)
    fields = models.ManyToManyField(Fields, blank=True)

    def __str__(self):
        return self.title + " @ " + self.company.name


class WorkSubmit(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    person = models.ForeignKey(PersonProfile, on_delete=models.CASCADE)

