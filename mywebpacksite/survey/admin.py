from django.contrib import admin

from .models import Question, Choice, LocationInfo, Participants, DailyReport, DailyTracker
# Register your models here.

class ChoiceInline(admin.StackedInline):
    model=Choice
    extra=3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

class ParticipantInline(admin.TabularInline):
    model=Participants
    extra=3

class DailyTrackerInline(admin.TabularInline):
    model=DailyTracker
    extra=3

class DailyReportInline(admin.TabularInline):
    model=DailyReport
    extra=0

class LocationInfoAdmin(admin.ModelAdmin):
    list_display = ('site_id', 'start_date')
    inlines = [ParticipantInline, DailyTrackerInline]

class DailyTrackerAdmin(admin.ModelAdmin):
    list_display = ('location', 'creation_date', 'modification_date')
    inlines = [DailyReportInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(LocationInfo, LocationInfoAdmin)
admin.site.register(DailyTracker, DailyTrackerAdmin)

