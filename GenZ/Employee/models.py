from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    domain_name = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=False, default='Canada')

    def __str__(self):
        return self.domain_name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Split the domain of the organization from the user's email
        domain = str(self.user.email).split('@')[1].split('.')[0]
        org, created = Organization.objects.get_or_create(domain_name=domain)
        self.organization = org
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email
