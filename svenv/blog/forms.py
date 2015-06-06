from django import forms
from django.conf import settings
from django.core.validators import validate_email
from smtplib import SMTP


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'test'}))
    email = forms.CharField(validators=[validate_email], widget=forms.TextInput(attrs={'placeholder': 'test'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'test'}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {'required': 'Name is required'}
        self.fields['email'].error_messages = {'required': 'E-mail is required'}
        self.fields['message'].error_messages = {'required': 'A message is required'}

    def send_email(self):
        data = self.cleaned_data
        name =  data['name']
        email =  data['email']
        message = data['message']

        smtp = SMTP(settings.SMTP_HOST)
        subject = 'Subject: %s: message from %s <%s>' % (settings.BLOG_TITLE, name, email)
        body = '%s\n\n%s' % (subject, message)
        smtp.sendmail(settings.EMAIL_FROM, settings.EMAIL, body)