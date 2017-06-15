import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) and self.pub_date <= timezone.now()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class LocationInfo(models.Model):
    site_id = models.CharField(max_length=16)
    condition = models.CharField(max_length=8)
    start_date = models.DateTimeField('study start date')

    def __str__(self):
        return self.site_id

class Participants(models.Model):
    location = models.ForeignKey(LocationInfo, on_delete=models.CASCADE)
    participant_name = models.CharField(max_length=32)
    participant_initials = models.CharField(max_length=4)

    def __str__(self):
        return self.participant_name

class DailyTracker(models.Model):
    location = models.ForeignKey(LocationInfo, on_delete=models.CASCADE)
    creation_date = models.DateTimeField('date created')
    modification_date = models.DateTimeField('date modified')

    def __str__(self):
        return self.creation_date

class DailyReport(models.Model):
    location = models.ForeignKey(DailyTracker, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participants)
    transitioned_well = models.BooleanField(default=False)
    asked_why_questions = models.IntegerField(default=0)
    creative_play = models.IntegerField(default=0)
    listened_well = models.IntegerField(default=0)
    not_there = models.BooleanField(default=False)

    def __str__(self):
        return self.location + "_" + self.participant
