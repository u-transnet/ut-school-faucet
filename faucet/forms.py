import re

from django import forms
from django.core.exceptions import ValidationError

from faucet.models import Lecture, Account


class RegistrationForm(forms.Form):

    name = forms.CharField(max_length=150)
    owner_key = forms.CharField(max_length=512)
    active_key = forms.CharField(max_length=512)
    memo_key = forms.CharField(max_length=512)
    access_token = forms.CharField(max_length=2048)
    social_network = forms.ChoiceField(choices=Account.NETWORKS)

    registrar = forms.CharField(max_length=255, required=False)
    referrer = forms.CharField(max_length=255, required=False)


class AddLectureForm(forms.Form):
    account_name = forms.CharField()
    topic_url = forms.URLField()
    access_token = forms.CharField()

    def clean(self):
        topic_id = self.get_topic_id()
        if not topic_id:
            raise ValidationError('Invalid url was provided %s' % self.cleaned_data.get('topic_url', ''))

        return self.cleaned_data

    def get_topic_id(self):
        if not self.cleaned_data:
            return None

        results = re.compile('topic-(\d+_\d+)').search(self.cleaned_data.get('topic_url', ''))
        if not results:
            return None

        return results.groups(1)


class GetLecturesForm(forms.Form):
    accounts = forms.CharField()

    def clean_accounts(self):
        accounts_names = self.cleaned_data['accounts'].split(',')
        return [account.strip() for account in accounts_names]
