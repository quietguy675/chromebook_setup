import os
from django.conf import settings
from django import forms
from django.forms import ModelForm
from survey.models import Location, Participant, DailyReport

class ReviewLocationForm(forms.Form):
    site_info = forms.ModelChoiceField(queryset=Location.objects.all())

class ReviewDayForm(forms.Form):
    day_info = forms.ChoiceField()
    def __init__(self, choices=(), *args, **kwargs):
        super(ReviewDayForm, self).__init__(*args, **kwargs)
        self.fields['day_info'].choices = choices

class LocationForm(forms.Form):
    site_id = forms.CharField(max_length=16)
    condition = forms.ChoiceField(choices=(
        ("control", "Control"),
        ("dtl", "DTL"),
        ("dtl_plus", "DTL+"),
        )
    )
    start_date = forms.DateField(help_text="mm/dd/yyyy")


surveyformchoices = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
)
surveyformparticipants = (
    ('bill', 'bill'),
    ('jim', 'jim'),
    ('bob', 'bob'),
)
class SurveyForm(forms.Form):
    participant = forms.CharField(disabled=True)
    transitioned_well = forms.ChoiceField(choices=surveyformchoices)
    asked_why_questions = forms.ChoiceField(choices=surveyformchoices)
    creative_play = forms.ChoiceField(choices=surveyformchoices)
    listened_well = forms.ChoiceField(choices=surveyformchoices)
    not_there = forms.BooleanField(required=False)

class AttendanceForm(forms.Form):
    participant = forms.CharField(disabled=True)
    present = forms.BooleanField(required=False)

class VideoForm(forms.Form):
    video_location = forms.FileField(widget=forms.HiddenInput, required=False)
    image_location = forms.FileField(widget=forms.HiddenInput, required=False)
    video_id = forms.IntegerField(widget=forms.HiddenInput)

class TimeForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()

