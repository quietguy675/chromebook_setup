import datetime
import csv
import os
from collections import OrderedDict
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from survey.forms import SurveyForm, ReviewLocationForm, ReviewDayForm, LocationForm, AttendanceForm, VideoForm, TimeForm
from django.forms import formset_factory
from survey.models import Location, Participant, DailyReport, VideoRecord, Attendance, Video
from django.conf import settings

def get_week_beginning():
    this_week = timezone.now().isocalendar()[1]
    past_week = timezone.now() - datetime.timedelta(days=7)
    while past_week.isocalendar()[1] < this_week:
        past_week = past_week + datetime.timedelta(days=1)
    return past_week

def sd_card_exists(fn):
    def wrapper(*args, **kwargs):
        if not (os.path.isdir(settings.VIDEO_LOCATION) and os.path.isdir(settings.IMAGE_LOCATION) and os.path.isdir(settings.RECORDED_VID_LOCATION)):
            return HttpResponseRedirect(reverse('survey:no_sd_card'))
        return fn(*args, **kwargs)
    return wrapper

def time_is_accurate(fn):
    def wrapper(*args, **kwargs):
        if datetime.datetime.now().date() < Location.objects.all().first().start_date:
            return HttpResponseRedirect(reverse('survey:time_is_off'))
        return fn(*args, **kwargs)
    return wrapper

def write_record(model, target_dirs=[], extra_columns={}, *args, **kwargs):
    all_rows = model.objects.all()
    row_headers = [x.name for x in model._meta.fields]
    writers = [csv.writer(x) for x in target_dirs]
    # Write headers
    for writer in writers:
        writer.writerow(list(extra_columns.keys()) + row_headers)
    temp = []
    for row in all_rows:
        for writer in writers:
            temp = list(extra_columns.values())
            temp = temp + [getattr(row, x) for x in row_headers]
            writer.writerow(temp)

def export_report_data(request):
    response = HttpResponse(content_type='text/csv')
    filename = 'report_data_' + str(timezone.now().date()) + '.csv'
    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
    
    # Open a directory to dump everything, write to both at same time.
    with open(settings.REPORT_EXPORT, 'w') as writefile:
        write_record(model=DailyReport, target_dirs=[writefile, response])
    return response

def export_attendance_data(request):
    response = HttpResponse(content_type='text/csv')
    filename = 'report_data_' + str(timezone.now().date()) + '.csv'
    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
    
    # Open a directory to dump everything, write to both at same time.
    with open(settings.ATTENDANCE_EXPORT, 'w') as writefile:
        write_record(model=Attendance, target_dirs=[writefile, response])
    return response
    

def export_video_data(request):
    response = HttpResponse(content_type='text/csv')
    filename = 'video_data_' + str(timezone.now().date()) + '.csv'
    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
    
    # Open a directory to dump everything, write to both at same time.
    locations = Location.objects.all()
    location = None
    extra_columns = {}
    if len(locations) == 1:
        location = locations[0]
        extra_columns = {'Test Condition': location.condition,
            'Study Start Date': location.start_date,
            'Site Name': str(location)
        }
    with open(settings.VIDEO_WATCH_EXPORT, 'w') as writefile:
        write_record(model=VideoRecord, target_dirs=[writefile, response], extra_columns=extra_columns)
    return response
    

@sd_card_exists
def review_data(request):
    other_nonsense = ''
    location = None
    day = None
    query = None
    if request.method == 'GET':
        location_form = ReviewLocationForm(request.GET)
        day_form = ReviewDayForm(request.GET)
        if location_form.is_valid():
            location = Location.objects.get(pk=request.GET['site_info'])
            something = location.dailyreport_set.values_list('last_mod_date')
            dates = [x[0].date() for x in something]
            clean_dates = []
            for date in dates:
                if date not in clean_dates:
                    clean_dates.append(date)
            clean_dates = [(x, str(x)) for x in clean_dates]
            day_form = ReviewDayForm(choices=clean_dates)
            if 'day_info' in request.GET:
                if request.GET['day_info']:
                    location = location_form.cleaned_data['site_info']
                    day = request.GET['day_info']
                    query = location.dailyreport_set.filter(last_mod_date__date=request.GET['day_info'])
        else:       
            day_form = ReviewDayForm()
    context = {'site_form': location_form,
        'day_form': day_form,
        'other_nonsense': other_nonsense,
        'site': location,
        'day': day,
        'query': query,
    }               
    return render(request, 'survey/review_data.html', context)


@time_is_accurate
@sd_card_exists
def survey_form(request):
    transposed_form = OrderedDict()    
    do_form = True
    all_participants = Participant.objects.all()
    # the model automatically converts to local timezone, so use datetime.
    dailyreport_done = len(DailyReport.objects.filter(last_mod_date__date=datetime.datetime.now().date())) > 0
    attendance_report_done = len(Attendance.objects.filter(mod_date__date=datetime.datetime.now().date())) > 0
    video_report_done = len(VideoRecord.objects.filter(watch_date__date=datetime.datetime.now().date())) > 0
 
    if dailyreport_done and attendance_report_done and video_report_done:
        do_form = False
    elif dailyreport_done and attendance_report_done:
        return HttpResponseRedirect(reverse('survey:video'))
    elif dailyreport_done and video_report_done:
        return HttpResponseRedirect(reverse('survey:attendance'))

    # get the number of surveys, add 1 so it is 1-indexed instead of 0-indexed
    num_surveys = len(DailyReport.objects.filter(last_mod_date__gte=get_week_beginning()).filter(last_mod_date__lte=timezone.now()))
    if len(all_participants):
        num_surveys = num_surveys / len(all_participants)
    num_surveys = int(num_surveys + 1)
    
    SurveyFormset = formset_factory(SurveyForm, extra=0)

    participant_names = [{'participant': x.participant_initials} for x in all_participants]
    if request.method == 'POST':
        formset = SurveyFormset(request.POST, request.FILES, initial=participant_names)
        if formset.is_valid():
            location = Location.objects.all()[0]
            for entry in formset.cleaned_data:
                # convert the participants object to an object
                entry['participant'] = Participant.objects.filter(participant_initials=entry['participant'])[0]
                entry['location']=location
                entry['last_mod_date']=timezone.now()
                dr = DailyReport(**entry)
                dr.save()
            with open(settings.REPORT_EXPORT, 'w') as writefile:
                write_record(model=DailyReport, target_dirs=[writefile])
            return HttpResponseRedirect(reverse('survey:attendance'))
    else:
        formset = SurveyFormset(initial=participant_names)
        for form in formset.forms:
            for field in form.visible_fields():
                if field.label not in transposed_form:
                    transposed_form[field.label] = [field]
                else:
                    transposed_form[field.label].append(field)

    context = {
        'do_form': do_form,
        'formset': formset,
        'transposed_form': transposed_form,
        'num_surveys': num_surveys,
    }
    return render(request, 'survey/survey.html', context)

@sd_card_exists
def attendance(request):
    # the model automatically converts to local timezone, so use datetime.
    if Attendance.objects.filter(mod_date__date=datetime.datetime.now().date()):
        if VideoRecord.objects.filter(watch_date__date=datetime.datetime.now().date()):
            return HttpResponseRedirect(reverse('survey:survey'))
        return HttpResponseRedirect(reverse('survey:video'))

    transposed_form = OrderedDict()    
    all_participants = Participant.objects.all()
    AttendanceFormset = formset_factory(AttendanceForm, extra=0) 
    participant_names = [{'participant': x.participant_initials, 'present':True} for x in all_participants]

    if request.method == 'POST':
        formset = AttendanceFormset(request.POST, request.FILES, initial=participant_names)
        if formset.is_valid():
            location = Location.objects.all()[0]
            for entry in formset.cleaned_data:
                # convert the participants object to an object
                entry['location'] = Location.objects.all().first()
                entry['participant'] = Participant.objects.filter(participant_initials=entry['participant'])[0]
                entry['mod_date']=timezone.now()
                dr = Attendance(**entry)
                dr.save()
            with open(settings.ATTENDANCE_EXPORT, 'w') as writefile:
                write_record(model=Attendance, target_dirs=[writefile])
            return HttpResponseRedirect(reverse('survey:video'))
    
    else:
        formset = AttendanceFormset(initial = participant_names) 
        for form in formset.forms:
            for field in form.visible_fields():
                if field.label not in transposed_form:
                    transposed_form[field.label] = [field]
                else:
                    transposed_form[field.label].append(field)

    context = {
        'formset': formset,
        'transposed_form': transposed_form,
    }
    
    return render(request, 'survey/attendance.html', context)

@sd_card_exists
def video(request, video_index=-1):
    # the model automatically converts to local timezone, so use datetime.
    if VideoRecord.objects.filter(watch_date__date=datetime.datetime.now().date()):
        return HttpResponseRedirect(reverse('survey:survey'))
    location = Location.objects.all().first()
    video = Video.objects.all().order_by('num_plays').first()
    form = VideoForm(initial={'video_id':video.id, 'video_location':video.video_location, 'image_location':video.image_location})
    if request.method == "POST":

        record_minutes = settings.VLC_THREAD_INSTANCE.stage_media_and_get_time_left(media=video.video_location, position=0.0)
        record_minutes += 120

        recorded_video = settings.FFMPEG_THREAD_INSTANCE.start_ffmpeg(save_location=settings.RECORDED_VID_LOCATION,
            date=timezone.now().date(),
            record_length=record_minutes)

        settings.VLC_THREAD_INSTANCE.start_vlc()

        video = Video.objects.filter(id=request.POST['video_id']).first()
        video.num_plays = video.num_plays + 1
        video.save()
        v = VideoRecord(location=location,
            video_recorded=recorded_video,
            video_played=video.video_location,
            watch_date=timezone.now())
        v.save()
        # Open a directory to dump everything, write to both at same time.
        extra_columns = {'Test Condition': location.condition,
            'Study Start Date': location.start_date,
            'Site Name': str(location)
        }
        with open(settings.VIDEO_WATCH_EXPORT, 'w') as writefile:
            write_record(model=VideoRecord,
                target_dirs=[writefile],
                extra_columns=extra_columns)
        return HttpResponseRedirect(reverse('survey:video'))
   
    context = {
        'image': os.path.split(video.image_location)[1],
        'description': video.description,
        'form': form,
    }
    return render(request, 'survey/video.html', context)

def no_sd_card(request):
    return render(request, 'survey/no_sd_card.html')

def time_is_off(request):
    if request.method == "POST":
        form = TimeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('survey:survey'))
    form = TimeForm(initial={"date": datetime.datetime.now().date, "time": datetime.datetime.now().time})
    context = {
        'form': form,
    }
    return render(request, 'survey/time_is_off.html', context)
