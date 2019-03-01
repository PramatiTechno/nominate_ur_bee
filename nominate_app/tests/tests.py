from django.test import TestCase
from django.urls import reverse, resolve
from nominate_app.views.create_award_view import awards
from nominate_app.models import Awards, NominationPeriod
from django.test.client import Client

# Create your tests here.

class AwardsTest(TestCase):

	def SetUp(self):
			self.client = Client()

	def test_awards_create(self):

		url = reverse('nominate_app:newawards')
		data = {
			'name': 'hello',
			'frequency':'QUATERLY',
			'nominationperiod_set-TOTAL_FORMS': '1', 
			'nominationperiod_set-INITIAL_FORMS': '0', 
			'nominationperiod_set-MIN_NUM_FORMS': '0', 
			'nominationperiod_set-MAX_NUM_FORMS': '1000', 
			'nominationperiod_set-0-level': '2', 
			'nominationperiod_set-0-start_day': '1', 
			'nominationperiod_set-0-end_day': '10', 
			'description': 'crshbd ghchufd'
		}

		response = self.client.post(url, data)
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, 'name')
		self.assertContains(response, 'frequency')
		self.assertContains(response, 'nominationperiod_set-TOTAL_FORMS')
		self.assertContains(response, 'nominationperiod_set-INITIAL_FORMS')
		self.assertContains(response, 'nominationperiod_set-MIN_NUM_FORMS')
		self.assertContains(response, 'nominationperiod_set-MAX_NUM_FORMS')
		self.assertContains(response, 'nominationperiod_set-0-level')
		self.assertContains(response, 'nominationperiod_set-0-start_day')
		self.assertContains(response, 'nominationperiod_set-0-end_day')
		self.assertContains(response, 'description')

	def test_csrf(self):
		url = reverse('nominate_app:newawards')
		response = self.client.get(url)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_awards_create_status_code(self):
		url = reverse('nominate_app:newawards')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_award_create_url_resolve(self):
		view = resolve('/newawards/')
		self.assertEquals(view.func, awards)