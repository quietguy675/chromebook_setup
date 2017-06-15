from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
from django.utils import timezone

from . import forms


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'survey/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """return the last five published questions published on or before today."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'survey/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'survey/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form.
        context = { 'question': question,
            'error_message': "you didn't select a choice."}
        return render(request, 'survey/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('survey:results', args=(question.id,)))

def test_form(request):
    form = forms.RegistrationForm(data=request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'survey/test_form.html', {'request': request, 'form': form})

class AdminInterface(generic.DetailView):
    template_name = 'survey/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return LocationInfo.objects.order_by('-start_date') 
