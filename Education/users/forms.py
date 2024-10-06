from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)
    #phone_number = forms.CharField(max_length=15, required=False, help_text='Enter your phone number')

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email',  'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        #user.phone_number = self.cleaned_data['phone_number']
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
    status = forms.ChoiceField(choices=[('student', 'Student'), ('tutor', 'Tutor')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status")

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    captcha = CaptchaField()  # Updated field for django-simple-captcha


class UserUpdateForm(forms.ModelForm):
    image=forms.FileField()
    email = forms.EmailField()
    designation = forms.ChoiceField(choices=[('student', 'Student'), ('others', 'Others')], required=False)
    address = forms.CharField(max_length=255, required=False, help_text='Enter your address')
    
    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 'last_name', 'email', 'image', 'description',
             'designation'
        ]
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'class': 'form-horizontal'}
        self.helper.label_class = 'col-md-3 col-form-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Field('first_name', css_class='form-control'),
            Field('last_name', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('image', css_class='form-control'),
            Field('description', css_class='form-control'),
            
            
            Field('designation', css_class='form-control'),
            
            Submit('submit', 'Update', css_class='btn btn-update'),
        )
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        
       
    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.social_media_links = {
            
        }
        if commit:
            user.save()
        return user


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = CaptchaField()  # Updated field for django-simple-captcha



