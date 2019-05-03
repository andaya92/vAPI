from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, APITestCase

from .views import *

from time import time
import datetime
from django.utils import timezone
from django.test import TestCase 
from .models import *
# Create your tests here.

TEST_IMG = "data:image/png;base64,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"

def populate_city_state():
	states = {
	"AZ" : ['Tempe', "Winslow"],
	"CA" : ['Atwater', "Manteca", "Modesto", "Ripon", "Sacramento"],
	}

	for state in states.keys():
		tmp_state = EventState()
		tmp_state.name = state
		tmp_state.save()
		for city in states[state]:
			tmp_city = EventCity()
			tmp_city.name = city
			tmp_city.state = tmp_state
			tmp_city.save()

class TestUser(APITestCase):
	def setUp(self):
		# Create two users
		User = get_user_model()
		User.objects.create_user("zeus", "test@g.com", "kidskids@2") # VolunteerProvier
		User.objects.create_user("hercules", "tester@g.com", "kidskids@2") # Volunteer
		
		#  Create VolunteerProvider
		vol_pro = VolunteerProvider()
		vol_pro.user_id = 1
		vol_pro.save()
		# Create Volunteer
		vol = Volunteer()
		vol.user_id = 2
		vol.save()

		# populate EventCity and EventState models
		populate_city_state()

		# Create VolunteerEvent
		event = VolunteerEvent()
		event.title = "Code4Cure"
		event.location_city_id = 1
		event.location_state_id = 1
		event.desc = "Code4purpose"
		event.details = "l2code"
		event.provider_id = 1
		event.event_begins = datetime.datetime.fromtimestamp(int(time()))
		event.event_ends = datetime.datetime.fromtimestamp(int(time())+1000)
		event.save()
		
	def test_view_create_user(self):
		# Create
		factory = APIRequestFactory()
		
		init_count = Volunteer.objects.count()
		request = factory.post('/home/account/new/',
								{'account_type' : 'volunteer',
								'username': 'godlike',
								'email' : 'g@g.com',
								'password' : 'kidskids@2',
								'password_confirm' : 'kidskids@2'})
		view = CreateUser.as_view()
		response = view(request)
		count = Volunteer.objects.count()
		
		self.assertEqual(init_count+1, count, "Volunteer not created, counts not equal")
		self.assertEqual(response.data['user']['username'], 'godlike', "Volunteer Usernames do not match")

		init_count = VolunteerProvider.objects.count()
		request = factory.post('/home/account/new/',
								{'account_type' : 'volunteer_provider',
								'username': 'ekildog',
								'email' : 'e@g.com',
								'password' : 'kidskids@2',
								'password_confirm' : 'kidskids@2'})

		response = view(request)
		count = VolunteerProvider.objects.count()
		
		self.assertEqual(init_count+1, count, "VolunteerProvider not created, counts not equal")
		self.assertEqual(response.data['user']['username'], 'ekildog', "Usernames do not match")

		# Delete User 
		User = get_user_model()
		init_count = User.objects.count()
		user = User.objects.create_user("t34t_u$34", "test@g.com", "letmein")
		response = self.client.delete("/home/account/delete/", {"pk":user.id})
		self.assertEqual(response.data['deleted'], True, "User not deleted when it should've")

		response = self.client.delete("/home/account/delete/", {"pk":-1})
		self.assertEqual(response.data['deleted'], False, "User deleted when it shouldn't've")

	def test_view_auth_user_API(self):
		factory = APIRequestFactory()
		request = factory.post('/home/auth_user/',
								{'email' : 'tester@g.com',
								'password': 'kidskids@2'})
		
		view = AuthUserAPI.as_view()
		response = view(request)
		self.assertEqual(response.data['user']['username'], 'hercules', "Username does not match user's email")
	def test_view_change_password(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		response = self.client.post("/home/change_password/", {
								"current_password": "kidskidz@2",
								"password": "chuckisgod1337",
								"password_confirm": "chuckisgod1337"
								})
		
		self.assertEqual(response.data['password_changed'], False)

		response = self.client.post("/home/change_password/", {
								"current_password": "kidskids@2",
								"password": "chuckisgod1337",
								"password_confirm": "chuckisgod1337"
								})
		self.assertEqual(response.data['password_changed'], True)
	def test_view_volunteer_API(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		response = self.client.get("/home/volunteer/all/")
		self.assertEqual(response.data[0]['user']['username'], "hercules", "Username does not match")

		response = self.client.get("/home/volunteer/pk/1/")
		self.assertEqual(response.data['user']['username'], "hercules", "Username does not match")		
		response = self.client.get("/home/volunteer/email/tester@g.com/")
		self.assertEqual(response.data['user']['username'], "hercules", "Username does not match")
	def test_view_volunteer_providers_API(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		response = self.client.get("/home/volunteer_provider/all/")
		self.assertEqual(response.data[0]['user']['username'], "zeus", "Username does not match")

		response = self.client.get("/home/volunteer_provider/pk/1/")
		self.assertEqual(response.data['user']['username'], "zeus", "Username does not match")

		response = self.client.get("/home/volunteer_provider/email/test@g.com/")
		self.assertEqual(response.data['user']['username'], "zeus", "Username does not match")

	def test_view_volunteer_event_API_get(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		response = self.client.get("/home/volunteer_event/pk/1/")		
		self.assertEqual(response.data['title'], "Code4Cure", "Title does not match record expected")

		response = self.client.get("/home/volunteer_event/city/1/")
		self.assertEqual(response.data[0]['title'], "Code4Cure", "Title does not match record expected")

		response = self.client.get("/home/volunteer_event/state/1/")
		self.assertEqual(response.data[0]['title'], "Code4Cure", "Title does not match record expected")

		response = self.client.get("/home/volunteer_event/provider/1/")
		self.assertEqual(response.data[0]['title'], "Code4Cure", "Title does not match record expected")
	def test_view_volunteer_event_API_post(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		init_count = VolunteerEvent.objects.count()
		response = self.client.post('/home/volunteer_event/new/',
								{'title' : 'My First Event',
								'desc': 'Its at my house',
								'event_state': '1',
								'event_city': '1',
								'details' : 'From 4:20',
								'provider' : '1',
								'event_begins' : int(time()), 
								'event_ends' : int(time())+1000})
		
		count = VolunteerEvent.objects.count()

		self.assertEqual(init_count+1, count, "VolunteerEvent not created, counts not equal")
		self.assertEqual(response.data['provider']['user']['username'], 'zeus', "VolunteerProvider Usernames do not match")
		self.assertEqual(response.data['title'], 'My First Event', "Volunteer Event Titles do not match")
	def test_view_volunteer_event_API_delete(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		# Create Provider
		provider_1 = self.client.post('/home/account/new/',
								{'account_type' : 'volunteer_provider',
								'username': 'ult_pr0v1dr',
								'email' : 'abc@g.com',
								'password' : 'kidskids@2',
								'password_confirm' : 'kidskids@2'})
		# Create Event
		provider_1_event = self.client.post('/home/volunteer_event/new/',
								{'title' : 'Sickest Vol Evt evr!!',
								'desc': 'Its at my house',
								'event_state': '1',
								'event_city': '1',
								'details' : 'From 4:20',
								'provider' : provider_1.data['id'],
								'event_begins' : int(time()), 
								'event_ends' : int(time())+1000})

		# Delete Event (Authentiacted user and Provider are not same, should not delete)
		is_deleted = self.client.delete("/home/volunteer_event/delete/", {"pk": provider_1_event.data['id']})
		self.assertEqual(is_deleted.data['deleted'], False)

		response = self.client.post('/home/volunteer_event/new/',
								{'title' : 'Sickest Vol Evt evr!!',
								'desc': 'Its at my house',
								'event_state': '1',
								'event_city': '1',
								'details' : 'From 4:20',
								'provider' : '1',
								'event_begins' : int(time()), 
								'event_ends' : int(time())+1000})
		
		is_deleted = self.client.delete("/home/volunteer_event/delete/", {"pk": response.data['id']})
		self.assertEqual(is_deleted.data['deleted'], True)


	def test_view_volunteer_post_get(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		# Create dummy post
		self.client.post("/home/volunteer_post/new/", {
								"user_id" : 1,
								"event_id" : 1,
								"img" : TEST_IMG,
								"caption" : "This is my first photo!"
								})
		
		# get dummy post by user_id
		response = self.client.get("/home/volunteer_post/user/1/")
		self.assertEqual(response.data[0]['caption'], "This is my first photo!", "Caption does not match")

		response = self.client.get("/home/volunteer_post/event/1/")
		self.assertEqual(response.data[0]['caption'], "This is my first photo!", "Caption does not match")
	def test_view_volunteer_post_post(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		init_count = VolunteerPost.objects.count()
		response = self.client.post("/home/volunteer_post/new/", {
								"user_id" : 1,
								# "event_id" : 1, # do not include if no event
								"img" : TEST_IMG,
								"caption" : "Second Photo!"
								})

		self.assertEqual(init_count+1, VolunteerPost.objects.count(), "Did not create post")
	def test_view_volunteer_post_delete(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		# Create post
		post = self.client.post("/home/volunteer_post/new/", {
								"user_id" : 2,
								# "event_id" : 1, # do not include if no event
								"img" : TEST_IMG,
								"caption" : "Not Zeus's Photo!"
								})

		is_deleted = self.client.delete('/home/volunteer_post/delete/', {'pk': post.data['id']})
		self.assertEqual(is_deleted.data['deleted'], False)

		# Create post
		post = self.client.post("/home/volunteer_post/new/", {
								"user_id" : zeus.id,
								# "event_id" : 1, # do not include if no event
								"img" : TEST_IMG,
								"caption" : "Zeus Photo!"
								})

		is_deleted = self.client.delete('/home/volunteer_post/delete/', {'pk': post.data['id']})
		self.assertEqual(is_deleted.data['deleted'], True)

	def test_view_volunteer_event_signup_API_post(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		response = self.client.post("/home/volunteer_event_signup/new/", {
											"volunteer_id" : 1,
											"event_id" : 1
											})

		self.assertEqual(response.data['event']['title'], "Code4Cure", "EVent titles does not match")
		self.assertEqual(response.data['volunteer']['user']['username'], "hercules", "Volunteer username does not match")	
	def test_view_volunteer_event_signup_API_get(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		response = self.client.post("/home/volunteer_event_signup/new/", {
											"volunteer_id" : 1,
											"event_id" : 1
											})

		response = self.client.get("/home/volunteer_event_signup/pk/1/")
		self.assertEqual(response.data['event']['title'], "Code4Cure", "Event Titles do not match")
		self.assertEqual(response.data['volunteer']['user']['username'], "hercules", "Volunteer Usernames do not match")

		response = self.client.get("/home/volunteer_event_signup/volunteer/1/")
		self.assertEqual(response.data[0]['event']['title'], "Code4Cure", "Event Titles do not match")
		self.assertEqual(response.data[0]['volunteer']['user']['username'], "hercules", "Volunteer Usernames do not match")

		response = self.client.get("/home/volunteer_event_signup/event/1/")
		self.assertEqual(response.data[0]['event']['title'], "Code4Cure", "Event Titles do not match")
		self.assertEqual(response.data[0]['volunteer']['user']['username'], "hercules", "Volunteer Usernames do not match")


	def test_view_volunteer_event_signup_API_delete(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))
		# Credentails are not the volunteers
		signup = self.client.post("/home/volunteer_event_signup/new/", {
											"volunteer_id" : 1,
											"event_id" : 1
											})
		# Try to delete
		is_deleted = self.client.delete("/home/volunteer_event_signup/delete/", {"pk" : signup.data['id']})
		# Expect Fail
		self.assertEqual(is_deleted.data['deleted'], False, "Signup deleted when it shoudln't've")

		# Change Credentails to volunteer that signed up for event
		hercules = get_user_model().objects.get(pk=2)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(hercules.rest_token))
		# Try to delete
		is_deleted = self.client.delete("/home/volunteer_event_signup/delete/", {"pk" : signup.data['id']})		
		# Expect deletion 
		self.assertEqual(is_deleted.data['deleted'], True, "Signup not deleted when it shoudl've")