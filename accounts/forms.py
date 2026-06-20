from django import forms
from .models import User, OtpCode, UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email','phone_number', 'full_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passwords don't match")
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text=
                                         "you can change password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login']


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(required=False, label='ایمیل (اختیاری)')
    full_name = forms.CharField(label='نام کامل')
    phone = forms.CharField(max_length=11, label='شماره موبایل')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('This phone number already exists')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                raise ValidationError('این ایمیل قبلاً ثبت شده است')
        return email



class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(label='ایمیل')
    full_name = forms.CharField(label='نام کامل')

    class Meta:
        model = UserProfile
        fields = ['address',]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['full_name'].initial = self.instance.user.full_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.user and self.user.email == email:
            return email
        if User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise ValidationError('این ایمیل قبلاً ثبت شده است')
        return email

    def save(self, commit=True):
        user = self.user
        user.full_name = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile


class PhoneNumberForm(forms.Form):
    phone = forms.CharField(max_length=11, label='شماره تلفن')