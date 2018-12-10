from django.db import models
from django.contrib.auth.models import User


class AppUser(User):
    user_type = models.CharField(max_length=5)


class Project(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    budget = models.IntegerField()


class Bids(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
    bid_amount = models.IntegerField()
    cover_letter = models.CharField(max_length=500)
    status = models.CharField(max_length=100, default="Pending")
    project_status = models.CharField(max_length=100, default="Not Hired")
