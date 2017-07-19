from django.contrib import admin

from .models import Location, Participant, DailyReport, VideoRecord, Video, Attendance
# Register your models here.
class ParticipantInline(admin.TabularInline):
    model=Participant
    extra=0

class VideosInline(admin.TabularInline):
    model=Video
    extra=0

class LocationAdmin(admin.ModelAdmin):
    list_display = ('site_id', 'start_date')
    inlines = [ParticipantInline, VideosInline]

class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('location', 'participant', 'last_mod_date')

class VideoRecordAdmin(admin.ModelAdmin):
    list_display = ('video_recorded', 'video_played', 'watch_date')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('participant', 'mod_date', 'present')

admin.site.register(Location, LocationAdmin)
admin.site.register(DailyReport, DailyReportAdmin)
admin.site.register(VideoRecord, VideoRecordAdmin)
admin.site.register(Attendance, AttendanceAdmin)
