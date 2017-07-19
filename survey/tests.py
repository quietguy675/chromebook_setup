import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question

# Create your tests here.
def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the
    given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('survey:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        create_question(question_text="Past question.", days = -30)
        response=self.client.get(reverse('survey:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    
    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed.
        """
        create_question(question_text="Future question.", days = 30)
        response = self.client.get(reverse('survey:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """
        Questions with a pub_date in the future are not displayed. Only past displayed
        """
        create_question(question_text="Future question.", days = 30)
        create_question(question_text="Past question.", days = -30)
        response = self.client.get(reverse('survey:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_question(self):
        """
        Questions in the past, also multiple, are displayed.
        """
        create_question(question_text="Past question1.", days = -30)
        create_question(question_text="Past question2.", days = -20)
        response = self.client.get(reverse('survey:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
            ['<Question: Past question2.>', '<Question: Past question1.>']
        )
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('survey:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the questions' text.
        """
        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse('survey:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns true for questions whose pub_date is recent.
        """
        time = timezone.now() - datetime.timedelta(hours=23, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)