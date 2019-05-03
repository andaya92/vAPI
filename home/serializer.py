from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('username', 'email')

class VolunteerSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Volunteer
		fields = "__all__"
		depth = 1

class VolunteerProviderSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = VolunteerProvider
		fields = "__all__"
		depth = 1	

class EventStateSerializer(serializers.ModelSerializer): 
	class Meta:
		model = EventState
		fields = "__all__"
		depth = 1	

class EventCitySerializer(serializers.ModelSerializer):
	state = EventStateSerializer()
	class Meta:
		model = EventCity
		fields = "__all__"
		depth = 1		

class VolunteerEventSerializer(serializers.ModelSerializer):
	provider = VolunteerProviderSerializer()
	location_state = EventStateSerializer()
	location_city = EventCitySerializer()
	
	class Meta:
		model = VolunteerEvent
		fields = "__all__"
		depth = 1	


class VolunteerPostSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	event = VolunteerEventSerializer()
	class Meta:
		model = VolunteerPost
		fields = "__all__"
		depth = 1


class VolunteerEventSignUpSerializer(serializers.ModelSerializer):
	volunteer = VolunteerSerializer()
	event = VolunteerEventSerializer()
	class Meta:
		model = VolunteerEventSignUp
		fields = "__all__"
		depth = 1

