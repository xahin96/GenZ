from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<organization_domain>/<filename>
    return f'{instance.organization.domain_name}/{filename}'


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
        org, created = Organization.objects.get_or_create(domain_name=domain, name = domain)
        self.organization = org
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email


class UploadedFile(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    upload_date = models.DateTimeField(auto_now_add=True)
    trained = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.file.name} uploaded by {self.uploaded_by.user.email}'


class Task(models.Model):
    STATUS_CHOICES = [
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
    ]
    task_title = models.CharField(max_length=100, unique=False)
    task_status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='RUNNING')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, blank=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.task_title


