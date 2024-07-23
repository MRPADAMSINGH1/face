from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox
from locations.models import Location
from .models import FaceRegistration


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())



class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

# New code start from here

class FaceRegistrationForm(forms.ModelForm):
    DESIGNATION_CHOICES = [
        ('1 year', '1 year'),
        ('2 years', '2 years'),
        ('3 years', '3 years'),
    ]

    ORGANIZATION_CHOICES = [
        ('IBM', 'IBM'),
        ('Edunet', 'Edunet'),
        ('DGT', 'DGT'),
    ]

    DIVISION_UNIT_CHOICES = [
        ('ADIT', 'ADIT'),
        ('IOT', 'IOT'),
        ('CSA', 'CSA'),
    ]

    designation = forms.ChoiceField(choices=DESIGNATION_CHOICES)
    organization = forms.ChoiceField(choices=ORGANIZATION_CHOICES)
    division_unit = forms.ChoiceField(choices=DIVISION_UNIT_CHOICES)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label=None)
    aadhar_id = forms.CharField(max_length=12, required=True)
    user_picture = forms.ImageField(required=True)  # New field

    class Meta:
        model = FaceRegistration
        fields = ['first_name', 'last_name', 'email', 'designation', 'mobile', 'organization', 'division_unit',
                  'location', 'aadhar_id', 'user_picture']

    def __init__(self, *args, **kwargs):
        super(FaceRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].disabled = True
        self.fields['last_name'].disabled = True
        self.fields['email'].disabled = True
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = False