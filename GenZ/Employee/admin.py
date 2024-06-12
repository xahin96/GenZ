from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import Employee, Organization

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'organization']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # Exclude superusers from the user dropdown
        self.fields['user'].queryset = User.objects.filter(is_superuser=False)

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    list_display = ('user', 'organization')
    search_fields = ('user__email', 'organization__name')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Organization)
