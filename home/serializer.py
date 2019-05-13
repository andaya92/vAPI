from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


class UserSerializer(serializers.ModelSerializer):
	acct_type = serializers.SerializerMethodField()
	class Meta:
		model = get_user_model()
		fields = ('username', 'email', 'id', 'acct_type')

	def get_acct_type(self, obj):
		acct_type = None
		try:
			acct_type = obj.volunteer
		except:
			print("Error, no volunteer")
		try:
			acct_type = obj.volunteerprovider
		except:
			print("Error, no provider")
			
		if type(acct_type) == type(Volunteer()):
			return "Volunteer"
		elif type(acct_type) == type(VolunteerProvider()):
			return "VolunteerProvider"
		return "None"

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

class DonationEventSerializer(serializers.ModelSerializer):
	class Meta:
			model = DonationEvent
			fields = "__all__"
			depth = 1


class UserDonationSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	event = DonationEventSerializer()
	class Meta:
			model = UserDonation
			fields = "__all__"
			depth = 1

class UserDonationRefundSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	event = DonationEventSerializer()
	class Meta:
			model = UserDonationRefund
			fields = "__all__"
			depth = 1