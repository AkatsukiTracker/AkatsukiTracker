from django.forms import ModelForm
from .models import *
from django import forms
from apps.users.models import Usuario
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class CheckUrlForm(ModelForm):
	class Meta:
		model = Producto
		fields = '__all__'

class ProductosForm(ModelForm):
	class Meta:
		model = Producto
		fields = '__all__'

class ImgPerfilForm(forms.Form):
	
	file = forms.FileField()

class SetEmailForm(forms.Form):
    """
    A form that lets a user change set their email without entering the old
    email
    """
    error_messages = {
        'email_mismatch': _("The two email fields didn't match."),
    }
    new_email1 = forms.CharField(label=_("New email"),
                                    widget=forms.EmailInput)
    new_email2 = forms.CharField(label=_("New email confirmation"),
                                    widget=forms.EmailInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetEmailForm, self).__init__(*args, **kwargs)

    def clean_new_email2(self):
        email1 = self.cleaned_data.get('new_email1')
        email2 = self.cleaned_data.get('new_email2')
        if email1 and email2:
            if email1 != email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return email2

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email1']
        if commit:
            self.user.save()
        return self.user

class EmailChangeForm(SetEmailForm):
    """
    A form that lets a user change their email by entering their old
    email.
    """
    error_messages = dict(SetEmailForm.error_messages, **{
        'email_incorrect': _("Your old email was entered incorrectly. "
                                "Please enter it again."),
    })
    old_email = forms.CharField(label=_("Old email"),
                                   widget=forms.EmailInput)

    def clean_old_email(self):
        """
        Validates that the old_email field is correct.
        """
        old_email = self.cleaned_data["old_email"]
        if old_email == self.user.email:
            raise forms.ValidationError(
                self.error_messages['email_incorrect'],
                code='email_incorrect',
            )
        return old_email
