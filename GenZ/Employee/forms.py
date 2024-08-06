from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, UploadedFile, Organization


class EmployeeSignupForm(forms.ModelForm):
    # username = forms.CharField(max_length =150, required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), required=True, )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Password", required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Confirm Password", required=True)

    class Meta:
        model = Employee
        fields = ('email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        employee = Employee(user=user)
        if commit:
            user.save()
            employee.save()
        return employee


class EmployeeLoginForm(forms.Form):
    # email = forms.EmailField(label="Email", required=True)
    email = forms.CharField(max_length =150, required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Password", required=True)


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'custom-file-input'})
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'website', 'address', 'city', 'province', 'postal_code', 'country', 'contact_name', 'contact_email', 'contact_phone']
        labels = {'province': 'Province/State'}