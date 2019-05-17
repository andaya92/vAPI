from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.views.generic.base import TemplateView
from django.db.utils import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from vAPI import settings
from .serializer import *

import base64
import stripe
import json
import feedparser
import pandas as pd
from datetime import datetime, timedelta


#######################
## Model Charts
########################

class index(TemplateView):
	template_name = "home/index.html"

class VolunteerChart(TemplateView):
	template_name = "home/volunteers.html"

	def get(self, request, volunteer=-1):
		self.template_name = "home/volunteers.html" if volunteer == 1 else "home/volunteer_providers.html"
		users = None
		total_users = 0
		if volunteer == 1:
			users = Volunteer.objects.all()
			total_users = Volunteer.objects.count()
		elif volunteer == 0:
			users = VolunteerProvider.objects.all()
			total_users = VolunteerProvider.objects.count()
		
		dat = pd.DataFrame()
		dat['dates'] = pd.to_datetime([user.user.date_joined for user in users])
		dat['count'] = [1 for user in users]
		dat = dat.set_index('dates', drop=False)
		dat = dat.resample("W").sum()

		context = {
			"dates" : [str(d) for d in dat.index],
			"count" : list(dat['count'].values),
			"total_users" : total_users
		}
		return render(request, self.template_name, context)

class VolunteerEventChart(TemplateView):
	template_name = "home/volunteer_events.html"

	def get(self, request):
		events = VolunteerEvent.objects.all()
		dat = pd.DataFrame()
		dat['dates'] = pd.to_datetime([event.event_begins for event in events])
		dat['count'] = [1 for event in events]
		dat = dat.set_index('dates', drop=False)
		dat = dat.resample("W").sum()

		context = {
			"total_events" : 50,
			"total_events_past" : 20,
			"total_events_future" : 30,
			"labels" : [str(d) for d in dat.index],
			"data" : list(dat['count'].values)

		}
		return render(request, self.template_name, context)


#######################
## Volunteer QuickQuestions
########################

class VolunteerInterestAPI(APIView):
	def get(self, request, pk=-1):
		interests = None
		if pk != -1:
			vol_int = VolunteerInterest.objects.get(pk=pk)
			return Response(VolunteerInterestSerializer(vol_int).data)
		else:
			interests = VolunteerInterest.objects.all()

		if interests:
			qr = list()
			for i in interests:
				qr.append(VolunteerInterestSerializer(i).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		name = request.data['name']
		desc = request.data['desc']
		try:
			vol_int = VolunteerInterest()
			vol_int.name = name
			vol_int.desc = desc
			vol_int.save()
			return Response(VolunteerInterestSerializer(vol_int).data)
		except:
			print("Failed to create Volunteer Interest {}".format(name))
		return Response({})

	def delete(self, request):
		pk = request.data['pk']
		try:
			obj = VolunteerInterest.objects.get(pk=pk)
			obj.delete()
			return Response({"deleted":True})
		except:
			print("Error deleting VolunteerInterest with pk: {}".format(pk))
		return Response({"deleted":False})

class UserVolunteerInterestAPI(APIView):
	def get(self, request, pk=-1, user_id=-1):
		interests = None
		if pk != -1:
			vol_int = UserVolunteerInterest.objects.get(pk=pk)
			return Response(UserVolunteerInterestSerializer(vol_int).data)
		elif user_id != -1:
			interests = UserVolunteerInterest.objects.filter(user_id=user_id)
		else:
			interests = UserVolunteerInterest.objects.all()

		if interests:
			qr = list()
			for i in interests:
				qr.append(UserVolunteerInterestSerializer(i).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		user_id = request.data['user_id']
		volunteer_interest_id = request.data['volunteer_interest_id']
		try:
			vol_int = UserVolunteerInterest()
			vol_int.user_id = user_id
			vol_int.volunteer_interest_id = volunteer_interest_id
			vol_int.save()
			return Response(UserVolunteerInterestSerializer(vol_int).data)
		except:
			print("Failed to create User Volunteer Interest")
		return Response({})

	def delete(self, request):
		pk = request.data['pk']
		try:
			obj = UserVolunteerInterest.objects.get(pk=pk)
			obj.delete()
			return Response({"deleted":True})
		except:
			print("Error deleting UserVolunteerInterest with pk: {}".format(pk))
		return Response({"deleted":False})

class VolunteerSkillAPI(APIView):
	def get(self, request, pk=-1):
		skills = None
		if pk != -1:
			vol_int = VolunteerSkill.objects.get(pk=pk)
			return Response(VolunteerSkillSerializer(vol_int).data)
		else:
			skills = VolunteerSkill.objects.all()

		if skills:
			qr = list()
			for i in skills:
				qr.append(VolunteerSkillSerializer(i).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		name = request.data['name']
		desc = request.data['desc']
		try:
			vol_int = VolunteerSkill()
			vol_int.name = name
			vol_int.desc = desc
			vol_int.save()
			return Response(VolunteerSkillSerializer(vol_int).data)
		except:
			print("Failed to create Volunteer Skill {}".format(name))
		return Response({})

	def delete(self, request):
		pk = request.data['pk']
		try:
			obj = VolunteerSkill.objects.get(pk=pk)
			obj.delete()
			return Response({"deleted":True})
		except:
			print("Error deleting VolunteerSkill with pk: {}".format(pk))
		return Response({"deleted":False})

class UserVolunteerSkillAPI(APIView):
	def get(self, request, pk=-1, user_id=-1):
		skills = None
		if pk != -1:
			vol_int = UserVolunteerSkill.objects.get(pk=pk)
			return Response(UserVolunteerSkillSerializer(vol_int).data)
		elif user_id != -1:
			skills = UserVolunteerSkill.objects.filter(user_id=user_id)
		else:
			skills = UserVolunteerSkill.objects.all()

		if skills:
			qr = list()
			for i in skills:
				qr.append(UserVolunteerSkillSerializer(i).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		user_id = request.data['user_id']
		volunteer_skill_id = request.data['volunteer_skill_id']
		try:
			vol_int = UserVolunteerSkill()
			vol_int.user_id = user_id
			vol_int.volunteer_skill_id = volunteer_skill_id
			vol_int.save()
			return Response(UserVolunteerSkillSerializer(vol_int).data)
		except:
			print("Failed to create User Volunteer Skill")
		return Response({})

	def delete(self, request):
		pk = request.data['pk']
		try:
			obj = UserVolunteerSkill.objects.get(pk=pk)
			obj.delete()
			return Response({"deleted":True})
		except:
			print("Error deleting UserVolunteerSkill with pk: {}".format(pk))
		return Response({"deleted":False})

#######################
## Account Features
########################

	# Returns dict w/ key 'error' True or False
		# 'msg' if error True
def check_password(password, password_confirm):
    hasChar = False
    hasNum = False
    if password != password_confirm:
    	return {"error":  True, "msg" : "Passwords do not match."}
    if len(password) < 8:
        return {"error":  True, "msg" : "Password must be 8 characters long..."}

    for c in password:
        if(type(c) == str):
            hasChar = True
        try:
            if(int(c) > -1 or int(c) < 10):
                hasNum = True
        except:
            pass
    if(not hasChar or not hasNum):
        return {"error": True, "msg" : "Must contain letters and numbers"}
    return {"error": False}

class CreateUser(APIView):
	
	def post(self, request):
		username = request.data['username']
		email = request.data['email']
		password = request.data['password']
		password_confirm = request.data['password_confirm']
		account_type = request.data['account_type']

		user = None
		account = None

		password_check = check_password(password, password_confirm)

		if not password_check['error']:
			try:
				user = User.objects.create_user(username, email, password)

				if account_type == "volunteer":
					account = Volunteer(user=user)
					account.save()
					return Response(VolunteerSerializer(account).data)
				elif account_type == "volunteer_provider":
					account = VolunteerProvider(user=user)
					account.save()
					return Response(VolunteerProviderSerializer(account).data)
				else:
					print("Error creating user")
					return Response({"error": "Account type error"})
			except IntegrityError as e:
				print("Error creating user {}".format(str(e)))
				print(e.args)
				return Response({"error":str(e)})
		elif password_check['error']:
			print(password_check['msg'])
		return Response({"error": "password check failed"})

	def delete(self, request):
		try:
			pk = request.data['pk']
			user = User.objects.get(pk=pk)
			user.delete()
			return Response({'deleted':True})
		except:
			return Response({'deleted':False})

class AuthUserAPI(APIView):
	def post(self, request):
		email = request.data['email']
		password = request.data['password']
		user = authenticate(email=email, password=password)
		if user:
			return Response({"user" : UserSerializer(user).data,
							"rest_token" : user.rest_token})
		return Response({})

class ChangePassword(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, special=None):
		current_password = request.data['current_password']
		password = request.data['password']
		password_confirm = request.data['password_confirm']
		checked_password = check_password(password, password_confirm)
		if not checked_password['error'] and request.user.check_password(current_password):
			request.user.set_password(password)
			return Response({"password_changed":True})
		elif checked_password['error']:
			print(checked_password['msg'])
		return Response({"password_changed":False})

class VolunteerAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, pk=-1, email=None):
		if pk != -1:
			vol = Volunteer.objects.get(pk=pk)
			return Response(VolunteerSerializer(vol).data)
		elif email:
			user = get_user_model().objects.filter(email=email)[0]
			if user:
				vol = Volunteer.objects.filter(user=user)[0]
				return Response(VolunteerSerializer(vol).data)
		else:
			volunteers = Volunteer.objects.all()
			qr = list()
			for v in volunteers:
				qr.append(VolunteerSerializer(v).data)
			return Response(qr)
		return Response({})

class VolunteerProviderAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	
	def get(self, request, pk=-1, email=None):
		if pk != -1:
			vol = VolunteerProvider.objects.get(pk=pk)
			return Response(VolunteerProviderSerializer(vol).data)
		elif email:
			user = get_user_model().objects.filter(email=email)[0]
			if user:
				vol = VolunteerProvider.objects.filter(user=user)[0]
				return Response(VolunteerProviderSerializer(vol).data)
		else:
			volunteers = VolunteerProvider.objects.all()
			qr = list()
			for v in volunteers:
				qr.append(VolunteerProviderSerializer(v).data)
			return Response(qr)
		return Response({})

class VolunteerEventAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, pk=-1, city=-1, state=-1, provider=-1):
		results = None
		if pk != -1:
			results = VolunteerEvent.objects.get(pk=pk)
			if results:
				return Response(VolunteerEventSerializer(results).data)
		elif state != -1:
			results = VolunteerEvent.objects.filter(location_state_id=state)
		elif city != -1:
			results = VolunteerEvent.objects.filter(location_city_id=city)
		elif provider != -1:
			results = VolunteerEvent.objects.filter(provider_id=provider)
		if results:
			qr = list() # list of query results
			for r in results:
				qr.append(VolunteerEventSerializer(r).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		title = request.data['title']
		state = request.data['event_state']
		city = request.data['event_city']
		desc = request.data['desc']
		details = request.data['details']
		provider = int(request.data['provider'])
		
		event_begins = int(request.data['event_begins'])
		event_ends = int(request.data['event_ends'])
		
		try:
			volunteer_event = VolunteerEvent()
			volunteer_event.title = title
			volunteer_event.location_state_id = state
			volunteer_event.location_city_id = city
			volunteer_event.desc = desc
			volunteer_event.details = details
			volunteer_event.provider_id = provider
			volunteer_event.event_begins = datetime.fromtimestamp(event_begins)
			volunteer_event.event_ends = datetime.fromtimestamp(event_ends)
			volunteer_event.save()
			return Response(VolunteerEventSerializer(volunteer_event).data)
		except:
			return Response({"error" : "event not created"})

	def delete(self, request):
		pk = request.data['pk']
		vol_event = VolunteerEvent.objects.get(pk=pk)
		if request.user.id == vol_event.provider.user_id:
			try:
				vol_event.delete()
				return Response({"deleted":True})
			except:
				print("Failed to delete event")
		return Response({"deleted":False})

class VolunteerPostAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, user_id=-1, event_id=-1):
		posts = None
		if user_id != -1:
			posts = VolunteerPost.objects.filter(user_id=user_id)
		elif event_id != -1:
			posts = VolunteerPost.objects.filter(event_id=event_id)

		if posts:
			qr = list()
			for p in posts:
				qr.append(VolunteerPostSerializer(p).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		user = request.data['user_id']
		event = None
		img = request.data['img'] # expects base64 encoded png
		png = None
		caption = request.data['caption']
		if "event_id" in request.data.keys():
			event = request.data['event_id']

		# Convert Image from png base64
		fmt, imgstr = img.split(';base64,') 
		ext = fmt.split('/')[-1] 
		# try:
		png = ContentFile(base64.b64decode(imgstr), name='{}_vol_post.{}'.format("usernameHere", ext))
		# except:
		#     error = "Could not create img for post"

		post = VolunteerPost()
		post.user_id = user
		post.event_id = event
		post.img = png
		post.caption = caption
		post.save()

		return Response(VolunteerPostSerializer(post).data)

	def delete(self, request):
		pk = request.data['pk']
		vol_post = VolunteerPost.objects.get(pk=pk)
		if request.user.id == vol_post.user.id:
			try:
				vol_post.delete()
				return Response({"deleted":True})
			except:
				print("Failed deleting Volunteer Post")
		return Response({"deleted":False})

class VolunteerEventSignUpAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, pk=-1, volunteer_id=-1, event_id=-1):
		results = None
		if pk != -1:
			vol_event_signup = VolunteerEventSignUp.objects.get(pk=pk)
			return Response(VolunteerEventSignUpSerializer(vol_event_signup).data)
		elif volunteer_id != -1:
			results = VolunteerEventSignUp.objects.filter(volunteer_id=volunteer_id)
		elif event_id != -1:
			results = VolunteerEventSignUp.objects.filter(event_id=event_id)
		qr = list()
		for r in results:
			qr.append(VolunteerEventSignUpSerializer(r).data)
		return Response(qr)

	def post(self, request):
		volunteer = request.data['volunteer_id']
		event = request.data['event_id']
		vol_event_signup = VolunteerEventSignUp()
		vol_event_signup.volunteer_id = volunteer
		vol_event_signup.event_id = event
		vol_event_signup.save()
		return Response(VolunteerEventSignUpSerializer(vol_event_signup).data)

	def delete(self, request):
		pk = request.data['pk']
		vol_ev_signup = VolunteerEventSignUp.objects.get(pk=pk)
		if vol_ev_signup.volunteer.user.id == request.user.id:
			try:
				vol_ev_signup.delete()
				return Response({"deleted":True})
			except:
				print("Failed deleting volunteer event signup")
		return Response({"deleted":False})


#######################
## Location
########################
class EventCityAPI(APIView):
	def get(self, request, pk=-1, name="none", state_id=-1, zipcode_id=-1):
		cities = None
		if pk != -1:
			city = EventCity.objects.get(pk=pk)
			return Response(EventCitySerializer(city).data)
		elif name != "none":
			cities = EventCity.objects.filter(name__contains=name)
		elif state_id != -1:
			cities = EventCity.objects.filter(state_id=state_id)
		elif zipcode_id != -1:
			cities = EventCity.objects.filter(zip_code_id=zipcode_id)
		else:
			cities = EventCity.objects.all()

		if cities:
			qr = list()
			for c in cities:
				qr.append(EventCitySerializer(c).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		name = request.data['name']
		state_id = request.data['state_id']
		zipcode_id = request.data['zipcode_id']
		city = None
		# try:
		city = EventCity()
		city.name = name
		city.state_id = state_id
		city.zip_code_id = zipcode_id
		city.save()
		# except:
		# 	print("Error creating City {}".format(name))
		if city:
			return Response(EventCitySerializer(city).data)
		return Response({})

	def delete(self, request):
		pk = request.data['pk']
		try:
			obj = EventCity.objects.get(pk=pk)
			obj.delete()
			return Response({"deleted":True})
		except:
			print("Error deleting EventCity with pk: {}".format(pk))
		return Response({"deleted":False})

class ZipCodeAPI(APIView):
	def get(self, request, pk=-1, name="none", state_id=-1):
		zipcodes = None
		if pk!=-1:
			zipcode = ZipCode.objects.get(pk=pk)
			return Response(ZipCodeSerializer(zipcode).data)
		elif name != "none":
			zipcodes = ZipCode.objects.filter(zip_code__contains=name)
		elif state_id != -1:
			zipcodes = ZipCode.objects.filter(state_id=name)
		else:
			zipcodes = ZipCode.objects.all()
		
		if zipcodes:
			qr = list()
			for z in zipcodes:
				qr.append(ZipCodeSerializer(z).data)
			return Response(qr)
		return Response({})


	def post(self, request):
		name = request.data['name']
		state_id = request.data['state_id']
		zipcode = None
		try:
			zipcode = ZipCode()
			zipcode.zip_code = name
			zipcode.state_id = state_id
			zipcode.save()
		except:
			print("Error creating ZipCode {}".format(name))
		if zipcode:
			return Response(ZipCodeSerializer(zipcode).data)
		return Response({})

	def delete(self, request):
		pk = request.data['pk']
		try:
			obj = ZipCode.objects.get(pk=pk)
			obj.delete()
			return Response({"deleted":True})
		except:
			print("Error deleting ZipCode with pk: {}".format(pk))
		return Response({"deleted":False})

class EventStateAPI(APIView):
	def get(self, request, pk=-1, name="none", country_id=-1):
		states = None
		if pk!=-1:
			state = EventState.objects.get(pk=pk)
			return Response(EventStateSerializer(state).data)
		elif name != "none":
			states = EventState.objects.filter(name__contains=name)
		elif country_id != -1:
			states = EventState.objects.filter(country_id=country_id)
		else:
			states = EventState.objects.all()
		
		if states:
			qr = list()
			for s in states:
				qr.append(EventStateSerializer(s).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		name = request.data['name']
		country_id = request.data['country_id']
		state = None
		try:
			state = EventState()
			state.name = name
			state.country_id = country_id
			state.save()
		except:
			print("Error creating State {}".format(name))
		if state:
			return Response(EventStateSerializer(state).data)
		return Response({})

	def delete(self, request):
		pk = request.data['pk']
		try:
			obj = EventState.objects.get(pk=pk)
			obj.delete()
			return Response({"deleted":True})
		except:
			print("Error deleting EventState with pk: {}".format(pk))
		return Response({"deleted":False})

class EventCountryAPI(APIView):
	def get(self, request, pk=-1, name="none"):
		countries = None
		if pk!=-1:
			country = EventCountry.objects.get(pk=pk)
			return Response(EventCountrySerializer(country).data)
		elif name != "none":
			countries = EventCountry.objects.filter(name__contains=name)
		else:
			countries = EventCountry.objects.all()
		
		if countries:
			qr = list()
			for c in countries:
				qr.append(EventCountrySerializer(c).data)
			return Response(qr)
		return Response({})

	def delete(self, request):
		pk = request.data['pk']
		try:
			obj = EventCountry.objects.get(pk=pk)
			obj.delete()
			return Response({"deleted":True})
		except:
			print("Error deleting EventCountry with pk: {}".format(pk))
		return Response({"deleted":False})


	def post(self, request):
		name = request.data['name']
		country = None
		try:
			country = EventCountry()
			country.name = name
			country.save()
		except:
			print("Error creating country {}".format(name))
		if country:
			return Response(EventCountrySerializer(country).data)
		return Response({})



#######################
## Donation Features
########################
class DonationEventAPI(APIView):
	def get(self, request, pk=-1, field=None, query=None):
		results = None
		if pk != -1:
			result = DonationEvent.objects.get(pk=pk)
			return Response(DonationEventSerializer(result).data)
		elif field and query:
			if field == "title":
				results = DonationEvent.objects.filter(title__contains=query)
			elif field == "beneficiary":
				results = DonationEvent.objects.filter(beneficiary__contains=query)

		if results:
			qr = list()
			for r in results:
				qr.append(DonationEventSerializer(r).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		title = request.data['title']
		desc = request.data['desc']
		details = request.data['details']
		beneficiary = request.data['beneficiary']

		try:
			de = DonationEvent()
			de.title = title
			de.desc = desc
			de.details = details
			de.beneficiary = beneficiary
			de.save()
			return Response(DonationEventSerializer(de).data)
		except:
			print("Erro creating donation event")
		return Response({})

	def delete(self, request):
		pk = request.data['pk']
		try:
			event = DonationEvent.objects.get(pk=pk)
			event.delete()
			return Response({'deleted':True})
		except:
			print("Error deleting DonationEvent")
		return Response({'deleted':False})

class DonationAPI(APIView):
	def get(self, request, user_id=-1, event_id=-1, charge_id="none"):
		results = None
		if user_id != -1:
			results = UserDonation.objects.filter(user_id=user_id)
		elif event_id != -1:
			results = UserDonation.objects.filter(event_id=event_id)
		elif charge_id != "none":
			try:
				stripe.api_key = settings.STRIPE_API_KEY
				result = stripe.Charge.retrieve(charge_id)
				return Response(result)
			except:
				print("Failed getting charge by id from Stripe")

		if results:
			qr = list()
			for r in results:
				qr.append(UserDonationSerializer(r).data)
			return Response(qr)
		return Response({})

	def post(self, request):
		stripe.api_key = settings.STRIPE_API_KEY
		
		user_stripe_token = request.data['user_stripe_token']
		amount = request.data['amount']
		donation_event_id = request.data['donation_event_id']
		
		de = DonationEvent.objects.get(pk=int(donation_event_id))

		charge = None
		try:
			charge = stripe.Charge.create(
				amount=int(amount)*100,
				currency='usd',
				description='Example charge',
				statement_descriptor= "Volunteer Me",
				metadata={
					"username" : request.user.username,
					"email" : request.user.email,
					"charge_type" : "donation",
					"ids" : json.dumps({"donation_event": donation_event_id }),
					"info" : json.dumps({"title":de.title, "desc":de.desc,
					"details":de.details, "beneficiary" : de.beneficiary})
				},
				source= user_stripe_token
			)
		except stripe.error.CardError as e:
			# Since it's a decline, stripe.error.CardError will be caught
			body = e.json_body
			err  = body.get('error', {})

			print ("Status is: {}".format(e.http_status))
			print ("Type is: {}".format(err.get('type')))
			print ("Code is: {}".format(err.get('code')))
			# param is '' in this case
			print ("Param is: {}".format(err.get('param')))
			print ("Message is: {}".format(err.get('message')))
			return Response({"data":str(e)})
		except stripe.error.RateLimitError as e:
		# Too many requests made to the API too quickly
			return Response({"data":str(e)})
		except stripe.error.InvalidRequestError as e:
		# Invalid parameters were supplied to Stripe's API
			return Response({"data":str(e)})
		except stripe.error.AuthenticationError as e:
		# Authentication with Stripe's API failed
		# (maybe you changed API keys recently)
			return Response({"data":str(e)})
		except stripe.error.APIConnectionError as e:
		# Network communication with Stripe failed
			return Response({"data":str(e)})
		except stripe.error.StripeError as e:
		# Display a very generic error to the user, and maybe send
		# yourself an email
			return Response({"data":str(e)})
		except:
			return Response({"data":"Error creating charge"})
		
		if charge:
			if charge.paid:
				try:
					ud = UserDonation()
					ud.user_id = request.user.id
					ud.event_id = de.id
					ud.amount = amount
					ud.charge = charge.id
					ud.save()
				except:
					print("Failed creating UserDonation record")
					# send data in json format to database
					# make process that checks database for rows and trys to save them again...
				return Response(charge)
		return Response()

	def delete(self, request):
		charge_id = request.data['charge_id']
		stripe.api_key = settings.STRIPE_API_KEY
		re = None
		try:
			re = stripe.Refund.create(
				charge=charge_id
			)
		except stripe.error.InvalidRequestError as e:
			print("Error creating refund", str(e))
		if re:
			result = UserDonation.objects.filter(charge=charge_id).first()
			if result:
				try:		
					refund = UserDonationRefund()
					refund.user_id = result.user_id
					refund.event_id = result.event_id
					refund.amount = result.amount
					refund.refund = re.id
					refund.charge = charge_id
					refund.save()
					try:
						result.delete()
					except:
						print("Failed deleting UserDonation")
				except:
					print("Failed creating UserDonationRefund")
			return Response(re)
		return Response({})

class UserDonationRefundAPI(APIView):
	def get(self, request, charge_id="none", refund_id="none", live=0):
		stripe.api_key = settings.STRIPE_API_KEY
		if charge_id != "none":
			try:
				if live == 1:
					refunds = stripe.Refund.list(charge=charge_id)
					qr =list()
					for r in refunds.auto_paging_iter():
						qr.append(r)
					return Response(qr)
				else:
					refund = UserDonationRefund.objects.filter(charge=charge_id).first()
					return Response(UserDonationRefundSerializer(refund).data)
			except:
				print("Failed getting refund from api via charge_id")
		elif refund_id != "none":
			try:
				if live == 1:
					refund = stripe.Refund.retrieve(refund_id)
					return Response(refund)
				else:
					refund = UserDonationRefund.objects.filter(refund=refund_id).first()
					return Response(UserDonationRefundSerializer(refund).data)
			except:
				print("Failed getting refund from api via refund_id")
		return Response({})

#######################
## News Feed Features
########################
class NewsAPI(APIView):
	
	def build_query(self, city, state,keyword):
		query = None
		if city != "none":
			query = "+".join([keyword.replace(" ", "+"), state, city])
		else:
			query = "+".join([keyword.replace(" ", "+"), state])
		return query


	def get(self, request, city="none", state="California", keyword="State of Emergency"):
		news = None
		try:
			news = feedparser.parse("https://news.google.com/rss/search?q={}&hl=en-US&gl=US&ceid=US:en".format(self.build_query(city, state, keyword)))
		except:
			print("Failed to get rss feed")
		if news:
			return Response(news['entries'])
		return Response({})


#######################
## 
########################

- 