import datetime
import os
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
SITE_CONDITIONS = (
    ('tl', 'TL'),
    ('dtn', 'DTN'),
    ('dtn_plus', 'DTN+')
)

class Location(models.Model):
    site_id = models.CharField(max_length=16)
    condition = models.CharField(max_length=8, choices=SITE_CONDITIONS)
    start_date = models.DateField(help_text="mm/dd/yyyy")

    def __str__(self):
        return self.site_id

class Participant(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    participant_initials = models.CharField(max_length=4, unique=True)
    participant_name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.participant_initials

DAILY_REPORT_CHOICES = (
    (0, 'N/A'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
)
class DailyReport(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
    participant = models.ForeignKey(Participant, default=None)
    last_mod_date = models.DateTimeField('Last Modified Date')
    transitioned_well = models.IntegerField(choices=DAILY_REPORT_CHOICES, default=1, blank=True)
    asked_why_questions = models.IntegerField(choices=DAILY_REPORT_CHOICES, default=1, blank=True)
    creative_play = models.IntegerField(choices=DAILY_REPORT_CHOICES, default=1, blank=True)
    listened_well = models.IntegerField(choices=DAILY_REPORT_CHOICES, default=1, blank=True)
    not_there = models.BooleanField(default=False)

    def __str__(self):
        return self.location.__str__() + "_" + self.participant.__str__()
class Attendance(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
    participant = models.ForeignKey(Participant, default=None)
    present = models.BooleanField(default=False)
    mod_date = models.DateTimeField()

class VideoRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
    video_played = models.FilePathField(path=settings.VIDEO_LOCATION, blank=True)
    video_recorded = models.FilePathField(path=settings.IMAGE_LOCATION, blank=True)
    watch_date = models.DateTimeField()

class Video(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
    video_location = models.FilePathField(path=settings.VIDEO_LOCATION)
    image_location = models.FilePathField(path=settings.IMAGE_LOCATION, blank=True)
    description = models.TextField(blank=True)
    num_plays = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.video_location.__str__()
