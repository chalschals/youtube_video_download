from django import forms
from django.core import validators
from downloader.models import Youtube


class YoutubeForm1(forms.ModelForm):
    class Meta:
        model = Youtube
        fields = ("url",)
        # exclude = ('created_at',)


class YoutubeForm2(forms.ModelForm):
    class Meta:
        model = Youtube
        fields = ("url", "sourcttype", "resolution",)
