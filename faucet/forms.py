import re

from django import forms
from django.core.exceptions import ValidationError

from faucet.models import Lecture


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