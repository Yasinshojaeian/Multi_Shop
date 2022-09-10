from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'password', 'is_active', 'is_admin')
        

def validations_phone(value):
    if len(value) > 12:
        raise ValidationError('تلفن شما معتبر نمی باشد')
    if value[0] != '0':
        raise ValidationError('تلفن شما باید با 0 شروع بشود')



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Email Or Phone'} ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username[0] == "0":
            if len(username) > 11 :
                raise ValidationError(
                    'Invalid value: %(value)s is invaliad',
                    code='invalid',
                    params={'value': f'{username}'},
                )
            if username[0] != '0':
                self.add_error('phone','شماره شما باید با 09 شروع شود ')
            if username[1] != '9':
                p = username[1]
                raise ValidationError(
                            'Invalid value: %(value)s',
                            code='invalid',
                            params={'value': f'رقم دوم شماره شما باید به جای{p} عدد 9 باشد'},
                        )
        else :
           pass
        return username
    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if len(phone) > 11 :
    #         raise ValidationError(
    #             'Invalid value: %(value)s is invaliad',
    #             code='invalid',
    #             params={'value': f'{phone}'},
    #         )
    #     return phone
    # def clean_phone(self):
    #     cd = super().clean()
    #     phone = cd['phone']
    #     if len(phone) > 12:
    #         self.add_error('phone','Phone Is Not INvalid')
    #     if phone[0] != '0':
    #         self.add_error('phone','شماره شما باید با 09 شروع شود ')
    #     if phone[1] != '9':
    #         p = phone[1]
    #         raise ValidationError(
    #                     'Invalid value: %(value)s',
    #                     code='invalid',
    #                     params={'value': f'رقم دوم شماره شما باید به جای{p} عدد 9 باشد'},
    #                 )
    #     return phone
    # def clean(self):
    #     breakpoint()
    #     y = super(LoginForm, self).clean()
    #     cd = super().clean()
    #     phone = cd['phone']
    #     if len(phone) > 11 :
    #         raise ValidationError(
    #             'Invalid value: %(value)s is invaliad',
    #             code='invalid',
    #             params={'value': f'{phone}'},
    #         )
    
class RegistrForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'} ),validators=[validators.MaxLengthValidator(11)])
    
class CheckOtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'} ),validators=[validators.MaxLengthValidator(4)])
    