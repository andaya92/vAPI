from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, APITestCase

from .views import *

from time import time
import datetime
import json
from django.utils import timezone
from django.test import TestCase 
from .models import *
# To-DO
# upload user photo
# 
# Create your tests here.

TEST_IMG = "data:image/png;base64,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"

def populate_city_state():
	countries = {
		"United States"	: {
			"AZ" : {
				"89745" : ["Tempe", "Winslow"] 
			},
			"CA" : {
				"95382" : ['Atwater', "Manteca", "Modesto", "Ripon", "Sacramento"]	
			}
		}
	}

	for country in countries.keys():
		tmp_country = EventCountry()
		tmp_country.name = country
		tmp_country.save()
		for state in countries[country].keys():
			tmp_state = EventState()
			tmp_state.name = state
			tmp_state.country = tmp_country
			tmp_state.save()
			for zipcode in countries[country][state].keys():
				tmp_zipcode = ZipCode()
				tmp_zipcode.zip_code = zipcode
				tmp_zipcode.state = tmp_state
				tmp_zipcode.save()
				for city in countries[country][state][zipcode]:
					tmp_city = EventCity()
					tmp_city.name = city
					tmp_city.state = tmp_state
					tmp_city.zip_code = tmp_zipcode
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
		tags = {"tags" : ['skill1', 'interest1', 'skill2']}
		
		event = VolunteerEvent()
		event.title = "Code4Cure"
		event.location_city_id = 1
		event.location_state_id = 1
		event.desc = "Code4purpose"
		event.details = "l2code"
		event.tags = json.dumps(tags)
		event.provider_id = 1
		event.event_begins = datetime.datetime.fromtimestamp(int(time()))
		event.event_ends = datetime.datetime.fromtimestamp(int(time())+1000)
		event.save()
		
	# def test_view_create_user_delete_user(self):
	# # 	# Create
	# 	factory = APIRequestFactory()
		
	# 	init_count = Volunteer.objects.count()
	# 	response = self.client.post('/home/account/new/',
	# 							{'account_type' : 'volunteer',
	# 							'username': 'godlike',
	# 							'email' : 'g@ga.com',
	# 							'password' : 'kidskids@2',
	# 							'password_confirm' : 'kidskids@2'})
	
	# 	count = Volunteer.objects.count()
		
	# 	self.assertEqual(init_count+1, count, "Volunteer not created, counts not equal")
	# 	self.assertEqual(response.data['user']['username'], 'godlike', "Volunteer Usernames do not match")

	# 	init_count = VolunteerProvider.objects.count()
	# 	response = self.client.post('/home/account/new/',
	# 							{'account_type' : 'volunteer_provider',
	# 							'username': 'ekildog',
	# 							'email' : 'e@g.com',
	# 							'password' : 'kidskids@2',
	# 							'password_confirm' : 'kidskids@2'})

	
	# 	count = VolunteerProvider.objects.count()
		
	# 	self.assertEqual(init_count+1, count, "VolunteerProvider not created, counts not equal")
	# 	self.assertEqual(response.data['user']['username'], 'ekildog', "Usernames do not match")

	# 	# Delete User 
	# 	User = get_user_model()
	# 	init_count = User.objects.count()
	# 	user = User.objects.create_user("t34t_u$34", "t3st@g.com", "letmein")
	# 	response = self.client.delete("/home/account/delete/", {"pk":user.id})
	# 	self.assertEqual(response.data['deleted'], True, "User not deleted when it should've")

	# 	response = self.client.delete("/home/account/delete/", {"pk":-1})
	# 	self.assertEqual(response.data['deleted'], False, "User deleted when it shouldn't've")

	# def test_view_auth_user_API(self):
	# 	factory = APIRequestFactory()
	# 	request = factory.post('/home/auth_user/',
	# 							{'email' : 'tester@g.com',
	# 							'password': 'kidskids@2'})
		
	# 	view = AuthUserAPI.as_view()
	# 	response = view(request)
	# 	self.assertEqual(response.data['user']['username'], 'hercules', "Username does not match user's email")
	# def test_view_change_password(self):
	# # 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	response = self.client.post("/home/change_password/", {
	# 							"current_password": "kidskidz@2",
	# 							"password": "chuckisgod1337",
	# 							"password_confirm": "chuckisgod1337"
	# 							})
		
	# 	self.assertEqual(response.data['password_changed'], False)

	# 	response = self.client.post("/home/change_password/", {
	# 							"current_password": "kidskids@2",
	# 							"password": "chuckisgod1337",
	# 							"password_confirm": "chuckisgod1337"
	# 							})
	# 	self.assertEqual(response.data['password_changed'], True)
	# def test_view_volunteer_API(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	response = self.client.get("/home/volunteer/all/")
	# 	self.assertEqual(response.data['data'][0]['user']['username'], "hercules", "Username does not match")

	# 	response = self.client.get("/home/volunteer/pk/1/")
	# 	self.assertEqual(response.data['user']['username'], "hercules", "Username does not match")		
	# 	response = self.client.get("/home/volunteer/email/tester@g.com/")
	# 	self.assertEqual(response.data['user']['username'], "hercules", "Username does not match")
	# def test_view_volunteer_providers_API(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	response = self.client.get("/home/volunteer_provider/all/")
	# 	self.assertEqual(response.data['data'][0]['user']['username'], "zeus", "Username does not match")

	# 	response = self.client.get("/home/volunteer_provider/pk/1/")
	# 	self.assertEqual(response.data['user']['username'], "zeus", "Username does not match")

	# 	response = self.client.get("/home/volunteer_provider/email/test@g.com/")
	# 	self.assertEqual(response.data['user']['username'], "zeus", "Username does not match")

	def test_view_volunteer_event_API_get(self):
		# User that is requesting from API
		zeus = get_user_model().objects.get(pk=1)
		self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

		tagless_event = self.client.post('/home/volunteer_event/new/',
				{'title' : 'Post_tagless',
				'desc': 'Esta me casa',
				'event_state': '1',
				'event_city': '1',
				'details' : 'From 4:20',
				'provider' : '1',
				'tags' : "",
				'event_begins' : int(time()), 
				'event_ends' : int(time())+1000})
		
		# must at least have one space for a valid URL
		response = self.client.get("/home/volunteer_event/tag/{}/".format(" "))
		self.assertEqual(response.data['data'][0]['title'], "Post_tagless", "Title does not match record expected")

		for index in range(10):
			ts = {"tags" : ['skill_{}'.format(index), 'interest_{}'.format(index), 'skill_b_{}'.format(index)]}
			
			self.client.post('/home/volunteer_event/new/',
				{'title' : 'Post_{}'.format(index),
				'desc': '{}_Esta me casa'.format(index),
				'event_state': '1',
				'event_city': '1',
				'details' : 'From 4:20',
				'provider' : '1',
				'tags' : json.dumps(ts),
				'event_begins' : int(time()), 
				'event_ends' : int(time())+1000})


		response = self.client.get("/home/volunteer_event/pk/1/")		
		self.assertEqual(response.data['title'], "Code4Cure", "Title does not match record expected")

		response = self.client.get("/home/volunteer_event/city/1/")
		self.assertEqual(response.data['data'][0]['title'], "Code4Cure", "Title does not match record expected")

		response = self.client.get("/home/volunteer_event/state/1/")
		self.assertEqual(response.data['data'][0]['title'], "Code4Cure", "Title does not match record expected")
		
		response = self.client.get("/home/volunteer_event/provider/1/")
		self.assertEqual(response.data['data'][0]['title'], "Code4Cure", "Title does not match record expected")
		
		tags = {"tags" : ['skill_3', 'interest_5', 'skill_b_7']}
		response = self.client.get("/home/volunteer_event/tag/{}/".format(json.dumps(tags)))
		# in ANdroid
		#	MultiSelect for intersts and skills
		# Create JSONObject with key tags and value JSONArray which is a list of items form the mutliselect view
		# Should allow select of city based on user's State (UserQuickQquestions; UQQ)
		self.assertEqual(len(response.data['data']), 3, "Expected 3 records")



	# def test_view_volunteer_event_API_post(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	init_count = VolunteerEvent.objects.count()
	# 	tags = {"tags" : ['skill1', 'interest1', 'skill2']}

	# 	response = self.client.post('/home/volunteer_event/new/',
	# 							{'title' : 'My First Event',
	# 							'desc': 'Its at my house',
	# 							'event_state': '1',
	# 							'event_city': '1',
	# 							'details' : 'From 4:20',
	# 							'provider' : '1',
	# 							'tags' : json.dumps(tags),
	# 							'event_begins' : int(time()), 
	# 							'event_ends' : int(time())+1000})
		
	# 	count = VolunteerEvent.objects.count()
	# 	self.assertEqual(init_count+1, count, "VolunteerEvent not created, counts not equal")
	# 	self.assertEqual(response.data['provider']['user']['username'], 'zeus', "VolunteerProvider Usernames do not match")
	# 	self.assertEqual(response.data['title'], 'My First Event', "Volunteer Event Titles do not match")
	# 	self.assertEqual(json.loads(response.data['tags']), tags, "Volunteer Event Tags do not match")

	# 	print(json.loads(response.data['tags']), tags)


	# def test_view_volunteer_event_API_delete(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	# Create Provider
	# 	provider_1 = self.client.post('/home/account/new/',
	# 							{'account_type' : 'volunteer_provider',
	# 							'username': 'ult_pr0v1dr',
	# 							'email' : 'abc@g.com',
	# 							'password' : 'kidskids@2',
	# 							'password_confirm' : 'kidskids@2'})

	

	# 	# Create Event
	# 	provider_1_event = self.client.post('/home/volunteer_event/new/',
	# 							{'title' : 'Sickest Vol Evt evr!!',
	# 							'desc': 'Its at my house',
	# 							'event_state': '1',
	# 							'event_city': '1',
	# 							'details' : 'From 4:20',
	# 							'provider' : provider_1.data['user']['id'],
	# 							'event_begins' : int(time()), 
	# 							'event_ends' : int(time())+1000})

		

	# 	# Delete Event (Authentiacted user and Provider are not same, should not delete)
	# 	is_deleted = self.client.delete("/home/volunteer_event/delete/", {"pk": provider_1_event.data['id']})
	# 	self.assertEqual(is_deleted.data['deleted'], False)

	# 	response = self.client.post('/home/volunteer_event/new/',
	# 							{'title' : 'Sickest Vol Evt evr!!',
	# 							'desc': 'Its at my house',
	# 							'event_state': '1',
	# 							'event_city': '1',
	# 							'details' : 'From 4:20',
	# 							'provider' : '1',
	# 							'event_begins' : int(time()), 
	# 							'event_ends' : int(time())+1000})

	# 	is_deleted = self.client.delete("/home/volunteer_event/delete/", {"pk": response.data['id']})
	# 	self.assertEqual(is_deleted.data['deleted'], True)

	# def test_view_volunteer_post_get(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	# Create dummy post
	# 	self.client.post("/home/volunteer_post/new/", {
	# 							"user_id" : 1,
	# 							"event_id" : 1,
	# 							"img" : TEST_IMG,
	# 							"caption" : "This is my first photo!"
	# 							})
		
	# 	# get dummy post by user_id
	# 	response = self.client.get("/home/volunteer_post/user/1/")
	# 	self.assertEqual(response.data['data'][0]['caption'], "This is my first photo!", "Caption does not match")

	# 	response = self.client.get("/home/volunteer_post/event/1/")
	# 	self.assertEqual(response.data['data'][0]['caption'], "This is my first photo!", "Caption does not match")
	# 	print(response.data['img'])
	# def test_view_volunteer_post_post(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	init_count = VolunteerPost.objects.count()
	# 	response = self.client.post("/home/volunteer_post/new/", {
	# 							"user_id" : 1,
	# 							# "event_id" : 1, # do not include if no event
	# 							"img" : TEST_IMG,
	# 							"caption" : "Second Photo!"
	# 							})

	# 	response = self.client.post("/home/volunteer_post/new/", {
	# 							"user_id" : 2,
	# 							"event_id" : 0, # do not include if no event
	# 							"img" : TEST_IMG,
	# 							"caption" : "Second Photo!"
	# 							})

	# 	self.assertEqual(init_count+2, VolunteerPost.objects.count(), "Did not create post")
	# def test_view_volunteer_post_delete(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	# Create post
	# 	post = self.client.post("/home/volunteer_post/new/", {
	# 							"user_id" : 2,
	# 							# "event_id" : 1, # do not include if no event
	# 							"img" : TEST_IMG,
	# 							"caption" : "Not Zeus's Photo!"
	# 							})

	# 	is_deleted = self.client.delete('/home/volunteer_post/delete/', {'pk': post.data['id']})
	# 	self.assertEqual(is_deleted.data['deleted'], False)

	# 	# Create post
	# 	post = self.client.post("/home/volunteer_post/new/", {
	# 							"user_id" : zeus.id,
	# 							# "event_id" : 1, # do not include if no event
	# 							"img" : TEST_IMG,
	# 							"caption" : "Zeus Photo!"
	# 							})

	# 	is_deleted = self.client.delete('/home/volunteer_post/delete/', {'pk': post.data['id']})
	# 	self.assertEqual(is_deleted.data['deleted'], True)

	# def test_view_volunteer_event_signup_API_post(self):
	# 	# User that is requesting from API
	# 	hercules = get_user_model().objects.get(pk=2)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(hercules.rest_token))

	# 	response = self.client.post("/home/volunteer_event_signup/new/", {
	# 										"volunteer_id" : hercules.id,
	# 										"event_id" : 1
	# 										})

	# 	self.assertEqual(response.data['event']['title'], "Code4Cure", "EVent titles does not match")
	# 	self.assertEqual(response.data['volunteer']['user']['username'], "hercules", "Volunteer username does not match")	
	# def test_view_volunteer_event_signup_API_get(self):
	# 	# User that is requesting from API
	# 	hercules = get_user_model().objects.get(pk=2)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(hercules.rest_token))

	# 	response = self.client.post("/home/volunteer_event_signup/new/", {
	# 										"volunteer_id" : hercules.id,
	# 										"event_id" : 1
	# 										})

	# 	response = self.client.get("/home/volunteer_event_signup/pk/1/")
	
	# 	self.assertEqual(response.data['event']['title'], "Code4Cure", "Event Titles do not match")
	# 	self.assertEqual(response.data['volunteer']['user']['username'], "hercules", "Volunteer Usernames do not match")

	# 	response = self.client.get("/home/volunteer_event_signup/volunteer/{}/".format(hercules.id))
	# 	self.assertEqual(response.data['data'][0]['event']['title'], "Code4Cure", "Event Titles do not match")
	# 	self.assertEqual(response.data['data'][0]['volunteer']['user']['username'], "hercules", "Volunteer Usernames do not match")

	# 	response = self.client.get("/home/volunteer_event_signup/event/1/")
	# 	self.assertEqual(response.data['data'][0]['event']['title'], "Code4Cure", "Event Titles do not match")
	# 	self.assertEqual(response.data['data'][0]['volunteer']['user']['username'], "hercules", "Volunteer Usernames do not match")
	# def test_view_volunteer_event_signup_API_delete(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))
	# 	# Credentails are not the volunteers
	# 	signup = self.client.post("/home/volunteer_event_signup/new/", {
	# 										"volunteer_id" : 2,
	# 										"event_id" : 1
	# 										})
	# 	# Try to delete
	# 	is_deleted = self.client.delete("/home/volunteer_event_signup/delete/", {"pk" : signup.data['id']})
	# 	# Expect Fail
	# 	self.assertEqual(is_deleted.data['deleted'], False, "Signup deleted when it shoudln't've")

	# 	# Change Credentails to volunteer that signed up for event
	# 	hercules = get_user_model().objects.get(pk=2)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(hercules.rest_token))
	# 	# Try to delete
	# 	is_deleted = self.client.delete("/home/volunteer_event_signup/delete/", {"pk" : signup.data['id']})		
	# 	# Expect deletion 
	# 	self.assertEqual(is_deleted.data['deleted'], True, "Signup not deleted when it shoudl've")

	# def test_view_dontaion_event_API_post(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	response = self.client.post("/home/donation_event/new/", {
	# 		"title" : "The big nasty disaster that befell your fellow neighbor.",
	# 		"desc" : "A huge natural disaster has beseiged your neighboring town.",
	# 		"details" : "Over 800billion in damages, eveyone homeless...",
	# 		"beneficiary" : "Red Rover Robin Relief"
	# 		})
	# 	self.assertEqual(response.data['id'], 1, "Should be the first entry in table")
	# def test_view_dontaion_event_API_get(self):
	# 	# User that is requesting from API
	# 	zeus = get_user_model().objects.get(pk=1)
	# 	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	# 	response = self.client.post("/home/donation_event/new/", {
	# 		"title" : "Southern Califonia Fire Disaster",
	# 		"desc" : "A huge natural disaster has beseiged your neighboring town.",
	# 		"details" : "Fires. Everywhere. River of flames riveting through town.",
	# 		"beneficiary" : "Smokey Fire Bear"
	# 		})

	# 	response = self.client.post("/home/donation_event/new/", {
	# 		"title" : "Flood in Big Name Area.",
	# 		"desc" : "Dat wet wet here. Wetter the better they said...",
	# 		"details" : "Everything is soaked",
	# 		"beneficiary" : "Noah & Sons"
	# 		})

	# 	response = self.client.post("/home/donation_event/new/", {
	# 		"title" : "Terror in insert church/school/concert/airport/huge building/ here.",
	# 		"desc" : "So many ded. vry sad.",
	# 		"details" : "We need help, send monies...",
	# 		"beneficiary" : "Church of Saints"
	# 		})


	# 	response = self.client.get("/home/donation_event/pk/1/")
	# 	self.assertEqual(response.data['title'], "Southern Califonia Fire Disaster", "Wrong title; Expected different title")

	# 	response = self.client.get("/home/donation_event/title/in/")
	# 	self.assertEqual(len(response.data['data']), 2, "Should be 2 result")

	# 	response = self.client.get("/home/donation_event/beneficiary/church/")
	# 	self.assertEqual(len(response.data['data']), 1, "Should be 1 result")

		
	# def test_view_dontaion_event_API_delete(self):
	# 	response = self.client.post("/home/donation_event/new/", {
	# 		"title" : "The big nasty disaster that befell your fellow neighbor.",
	# 		"desc" : "A huge natural disaster has beseiged your neighboring town.",
	# 		"details" : "Over 800billion in damages, eveyone homeless...",
	# 		"beneficiary" : "Red Rover Robin Relief"
	# 		})
	# 	response = self.client.delete("/home/donation_event/delete/", {"pk" : response.data['id']})
	
	# def test_stripe_donation_system(self):
	# 	# 	# Make donation
	# 	# 	# 	# User that is requesting from API
	#  	zeus = get_user_model().objects.get(pk=1)
	#  	self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(zeus.rest_token))

	#  	donation_event = self.client.post("/home/donation_event/new/", {
	#  		"title" : "The big nasty disaster that befell your fellow neighbor.",
	#  		"desc" : "A huge natural disaster has beseiged your neighboring town.",
	#  		"details" : "Over 800billion in damages, eveyone homeless...",
	#  		"beneficiary" : "Red Rover Robin Relief"
	#  		})
	#  	donation = self.client.post("/home/make_donation/", {
	#  								"user_stripe_token": "tok_1EdAhiIgfiVd5gwh5eVmjyTV",
	#  								# "donation_event_id" : donation_event.data['id'],
	#  								"donation_event_id" : "-1", # rest of the test will fail because it expects a donation event to be created
	#  								"amount" : "7347.00"
	#  								})

	#  	print(donation.data)
	#  	self.assertEqual(donation.data['paid'], True, "Donation not paid")
		
	#  	# store charge_id
	#  	charge_id = donation.data['id']
	#  	self.assertEqual(charge_id[:3], "ch_", "Id is not a Stripe charge id")
		
	#  	# Get donation from DB
	#  	user_donations = self.client.get("/home/user_donation/user/1/")
	#  	# user_donations = self.client.get("/home/user_donation/event/1/")
	#  	print(user_donations.data)
	#  	self.assertEqual(user_donations.data['data'][0]['charge'], charge_id,
	#  						"Stripe chrage id is incorrect {} - {}."
	#  						.format(user_donations.data['data'][0]['charge'], charge_id))
		
	#  	user_donation_id = user_donations.data['data'][0]['id']

	# 	# 	# Refund donation
	#  	refund = self.client.delete("/home/refund_user_donation/", {"charge_id":charge_id})
	#  	self.assertEqual(refund.data['charge'], charge_id, "Stripe chrage id is incorrect {} - {}."
	#  						.format(refund.data['charge'], charge_id))


	# 	# 	# Get refund
	#  	refund = self.client.get("/home/user_donation_refund/charge/live/{}/0/".format(charge_id))
	 	
	#  	self.assertEqual(refund.data['user']['username'], "zeus", "Username does not match for refund")

	#   helper
	# def print_news(self, data):
	# 	# list of news entries
	# 	# <class 'feedparser.FeedParserDict'>
	# 	for e in data:
	# 		print("Entry Type:")
	# 		print(type(e))
	# 		print("Title: \n ---{}".format(e.title))
	# 		# California Governor Declares State of Emergency in Eight Counties, Including Mariposa County, Due to Winter Storms - Sierra Sun Times
	# 		print(e.link)
	# 		# https://goldrushcam.com/sierrasuntimes/index.php/news/local-news/18230-california-governor-declares-state-of-emergency-in-eight-counties-including-mariposa-county-due-to-winter-storms
	# 		print(e.summary)
	# 		print(e.published)
	# 		# <a href="https://goldrushcam.com/sierrasuntimes/index.php/news/local-news/18230-california-governor-declares-state-of-emergency-in-eight-counties-including-mariposa-county-due-to-winter-storms" target="_blank">California Governor Declares State of Emergency in Eight Counties, Including Mariposa County, Due to Winter Storms</a>&nbsp;&nbsp;<font color="#6f6f6f">Sierra Sun Times</font><p>April 13, 2019 - SACRAMENTO — Governor Gavin Newsom on Friday issued an emergency proclamation for the counties of Butte, Colusa, Del Norte, Mariposa, ...</p>'
	# 		print(e.source.href)
	# 		# https://goldrushcam.com
	# 		print(e.source.title)
	# 		# Sierra Sun Times
	# 		if "media_content" in e.keys():
	# 			# <class 'dict'>
	# 			for c in e.media_content:
	# 				print(c['url']) if "url" in c.keys() else print("no url")
	# 				# https://lh4.googleusercontent.com/proxy/jcPiFk6AIyqAwAhHEdYkxZrEBb0o5u8wm1nv_03hjYdjFHEstekQWFQmQS6dYdkEQo6QsQmFVGHzi31hf92yNVrLN54pMto3SPyOaeBLpRX1nuC-4nGwKZXz_1KKIedju_VB36E=-w150-h150-c
	# 				print(c['medium']) if "medium" in c.keys() else print("no medium")
	# 				# image
	# 		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	# def test_view_news_API(self):
	# 	city_state_news = self.client.get("/home/news/city/state/Sacramento/California/terror/")
	# 	state_news = self.client.get("/home/news/state/California/state of emergency/")
		
	# 	self.assertNotEqual(len(city_state_news.data), 0, "Feed length zero, no news returned")
	# 	self.assertNotEqual(city_state_news.data, None, "Feed == 'None' ")

	# 	# self.print_news(city_state_news.data)
	# 	# self.print_news(state_news.data)
		
	# def test_locations_API(self):
	# 	country = self.client.post("/home/location/country/new/", {"name" : 'USA'})

	# 	state = self.client.post("/home/location/state/new/", {"name" : 'New York',
	# 															"country_id" : country.data['id']
	# 															})

	# 	zipcode = self.client.post("/home/location/zipcode/new/", {"name" : '78945', 
	# 																"state_id" : state.data['id'],
	# 															})

	# 	city = self.client.post("/home/location/city/new/", {"name" : 'Manhatty',
	# 															"state_id" : state.data['id'],
	# 															"zipcode_id" : zipcode.data['id'],

	# 																})

	# 	self.assertEqual(country.data['name'], "USA", "Country name is not what was expected.")
	# 	self.assertEqual(state.data['name'], "New York", "State name is not what was expected.")
	# 	self.assertEqual(zipcode.data['zip_code'], "78945", "Zipcode is not what was expected.")
	# 	self.assertEqual(city.data['name'], "Manhatty", "City name is not what was expected.")


	# 	country = self.client.get("/home/location/country/")
	# 	state = self.client.get("/home/location/state/")
	# 	zipcode = self.client.get("/home/location/zipcode/")
	# 	city = self.client.get("/home/location/city/")
		
	# 	city_by_state = self.client.get("/home/location/city/state/{}/".format(state.data['data'][0]['id']))

	# 	self.assertEqual(len(country.data) > 0, True, "Expected more data from Country API.")
	# 	self.assertEqual(len(state.data) > 0, True, "Expected more data from State API.")
	# 	self.assertEqual(len(zipcode.data) > 0, True, "Expected more data from Zipcode API.")
	# 	self.assertEqual(len(city.data) > 0, True, "Expected more data from City API.")

	# 	country = self.client.get("/home/location/country/USA/")
	# 	state = self.client.get("/home/location/state/New York/")
	# 	zipcode = self.client.get("/home/location/zipcode/contains/789/")
	# 	city = self.client.get("/home/location/city/Man/")

	# 	self.assertEqual(len(country.data) > 0, True, "Expected more data from Country API.")
	# 	self.assertEqual(len(state.data) > 0, True, "Expected more data from State API.")
	# 	self.assertEqual(len(zipcode.data) > 0, True, "Expected more data from Zipcode API.")
	# 	self.assertEqual(len(city.data) > 0, True, "Expected more data from City API.")

	# 	country = self.client.get("/home/location/country/pk/1/")
	# 	state = self.client.get("/home/location/state/pk/1/")
	# 	zipcode = self.client.get("/home/location/zipcode/pk/1/")
	# 	city = self.client.get("/home/location/city/pk/1/")

	# 	self.assertEqual(len(country.data) > 0, True, "Expected more data from Country API.")
	# 	self.assertEqual(len(state.data) > 0, True, "Expected more data from State API.")
	# 	self.assertEqual(len(zipcode.data) > 0, True, "Expected more data from Zipcode API.")
	# 	self.assertEqual(len(city.data) > 0, True, "Expected more data from City API.")


	# 	city = self.client.delete("/home/location/city/delete/", {"pk" : city.data['id']})
	# 	zipcode = self.client.delete("/home/location/zipcode/delete/", {"pk" : zipcode.data['id']})
	# 	state = self.client.delete("/home/location/state/delete/", {"pk" : state.data['id']})
	# 	country = self.client.delete("/home/location/country/delete/", {"pk" : country.data['id']})

	# 	self.assertEqual(city.data['deleted'], True, "City not deleted")
	# 	self.assertEqual(zipcode.data['deleted'], True, "Zipcode not deleted")
	# 	self.assertEqual(state.data['deleted'], True, "State not deleted")
	# 	self.assertEqual(country.data['deleted'], True, "Country not deleted")

	# 	#######################
	# 	## User Quick Questions
	# 	########################

	# 	###############
	# 	# Interests
	# 	###############

	# def test_view_volunteer_interest_post(self):
	# 	interest = self.client.post("/home/interests/new/", {"name":"Helping", "desc":"You like hleping others"})

	# def test_view_volunteer_interest_get(self):
	# 	vol_interest = self.client.post("/home/interests/new/", {"name":"Helping", "desc":"You like hleping others"})
	# 	interest = self.client.get("/home/interests/pk/{}/".format(vol_interest.data['id']))
	# 	interests = self.client.get("/home/interests/")

	# 	deleted = self.client.delete("/home/interests/delete/", {"pk" : vol_interest.data['id']})
	# 	self.assertEqual(deleted.data['deleted'], True, "Data not deleted")

	# 	###############
	# 	# Skills
	# 	###############
	# def test_view_volunteer_skill_post(self):
	# 	skill = self.client.post("/home/skills/new/", {"name":"Helping", "desc":"You like hleping others"})

	# def test_view_volunteer_skill_get_delete(self):
	# 	vol_skill = self.client.post("/home/skills/new/", {"name":"Helping", "desc":"You like hleping others"})
	# 	skill = self.client.get("/home/skills/pk/{}/".format(vol_skill.data['id']))
	# 	skills = self.client.get("/home/skills/")

	# 	deleted = self.client.delete("/home/skills/delete/", {"pk" : vol_skill.data['id']})
	# 	self.assertEqual(deleted.data['deleted'], True, "Data not deleted")

	# 	###############
	# 	# User Interests
	# 	###############

	# def test_view_user_volunteer_interest_post(self):
	# 	interest = self.client.post("/home/interests/new/", {"name":"Helping", "desc":"You like hleping others"})
	# 	interest = self.client.post("/home/interests/user/new/", {"user_id":"1", "volunteer_interest_id": interest.data['id']})

	# def test_view_user_volunteer_interest_get_delete(self):
	# 	vol_interest = self.client.post("/home/interests/new/", {"name":"Helping", "desc":"You like hleping others"})
	# 	interest = self.client.post("/home/interests/user/new/", {"user_id":"1", "volunteer_interest_id": vol_interest.data['id']})
		
	# 	user_interest = self.client.get("/home/interests/user/pk/1/")
		
	# 	user_interests = self.client.get("/home/interests/user/1/")
	# 	all_user_interests_records = self.client.get("/home/interests/user/")

	# 	deleted = self.client.delete("/home/interests/user/delete/", {"pk" : interest.data['id']})
	# 	self.assertEqual(deleted.data['deleted'], True, "Data not deleted")

	# 	###############
	# 	# User Skills
	# 	###############

	# def test_view_user_volunteer_skill_post(self):
	# 	skill = self.client.post("/home/skills/new/", {"name":"Helping", "desc":"You like hleping others"})
	# 	skill = self.client.post("/home/skills/user/new/", {"user_id":"1", "volunteer_skill_id": skill.data['id']})


	# def test_view_user_volunteer_skill_get_delete(self):
	# 	vol_skill = self.client.post("/home/skills/new/", {"name":"Typing", "desc":"You like typing lots"})
	# 	skill = self.client.post("/home/skills/user/new/", {"user_id":"1", "volunteer_skill_id": vol_skill.data['id']})
		
	# 	user_skill = self.client.get("/home/skills/user/pk/1/")
		
	# 	user_skills = self.client.get("/home/skills/user/1/")
	# 	all_user_skills_records = self.client.get("/home/skills/user/")

		
	# 	deleted = self.client.delete("/home/skills/user/delete/", {"pk" : skill.data['id']})
	# 	self.assertEqual(deleted.data['deleted'], True, "Data not deleted")