from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from datetime import datetime

from .serializer import *

from django.core.files.base import ContentFile

import base64


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

# Create your views here.
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




class AuthUserAPI(APIView):
	def post(self, request):
		email = request.data['email']
		password = request.data['password']
		user = authenticate(email=email, password=password)
		if user:
			return Response({"user" : UserSerializer(user).data,
							"rest_token" : user.rest_token})
		return Response({})

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
					return Response({})
			except:
				print("Error creating user")
				return Response({})
		elif password_check['error']:
			print(password_check['msg'])

	def delete(self, request):
		try:
			pk = request.data['pk']
			user = User.objects.get(pk=pk)
			user.delete()
			return Response({'deleted':True})
		except:
			return Response({'deleted':False})

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
			volunteer_event.event_begins = datetime.datetime.fromtimestamp(event_begins)
			volunteer_event.event_ends = datetime.datetime.fromtimestamp(event_ends)
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
			print("getting posts by event")
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