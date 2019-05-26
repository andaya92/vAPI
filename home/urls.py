from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "home"
 
urlpatterns = [

	path("models/", views.index.as_view(), name="index"),
	path("models/users/<int:volunteer>/", views.VolunteerChart.as_view(), name="vol_chart"),
	path("models/volunteer_events/", views.VolunteerEventChart.as_view(), name="vol_event_chart"),
	####
	# API
	####
	# Accounts
	path("account/new/", views.CreateUser.as_view(), name="register"),
	path("account/delete/", views.CreateUser.as_view(), name="register"),
	path("auth_user/", views.AuthUserAPI.as_view(), name="auth_user"),
	path("change_password/", views.ChangePassword.as_view(), name="change_password"),
	#	Volunteers
	path("volunteer/all/", views.VolunteerAPI.as_view(), name="get_volunteer"),
	path("volunteer/pk/<int:pk>/", views.VolunteerAPI.as_view(), name="get_volunteer"),
	path("volunteer/email/<str:email>/", views.VolunteerAPI.as_view(), name="get_volunteer"),
	#	Providers
	path("volunteer_provider/all/", views.VolunteerProviderAPI.as_view(), name="get_volunteer_provider"),
	path("volunteer_provider/pk/<int:pk>/", views.VolunteerProviderAPI.as_view(), name="get_volunteer_provider"),
	path("volunteer_provider/email/<str:email>/", views.VolunteerProviderAPI.as_view(), name="get_volunteer_provider"),

	# Locations
	#	City
	path("location/city/new/", views.EventCityAPI.as_view(), name="event_city"),
	path("location/city/delete/", views.EventCityAPI.as_view(), name="event_city"),
	path("location/city/", views.EventCityAPI.as_view(), name="event_city"),
	path("location/city/pk/<int:pk>/", views.EventCityAPI.as_view(), name="event_city"),
	path("location/city/<str:name>/", views.EventCityAPI.as_view(), name="event_city"),
	path("location/city/state/<int:state_id>/", views.EventCityAPI.as_view(), name="event_city"),
	#	Zipcode
	path("location/zipcode/new/", views.ZipCodeAPI.as_view(), name="zipcode"),
	path("location/zipcode/delete/", views.ZipCodeAPI.as_view(), name="zipcode"),
	path("location/zipcode/", views.ZipCodeAPI.as_view(), name="zipcode"),
	path("location/zipcode/pk/<int:pk>/", views.ZipCodeAPI.as_view(), name="zipcode"),
	path("location/zipcode/contains/<int:name>/", views.ZipCodeAPI.as_view(), name="zipcode"),
	#	State
	path("location/state/new/", views.EventStateAPI.as_view(), name="event_state"),
	path("location/state/delete/", views.EventStateAPI.as_view(), name="event_state"),
	path("location/state/", views.EventStateAPI.as_view(), name="event_state"),
	path("location/state/pk/<int:pk>/", views.EventStateAPI.as_view(), name="event_state"),
	path("location/state/<str:name>/", views.EventStateAPI.as_view(), name="event_state"),
	#	Country
	path("location/country/new/", views.EventCountryAPI.as_view(), name="event_country"),
	path("location/country/delete/", views.EventCountryAPI.as_view(), name="event_country"),
	path("location/country/", views.EventCountryAPI.as_view(), name="event_country"),
	path("location/country/pk/<int:pk>/", views.EventCountryAPI.as_view(), name="event_country"),
	path("location/country/<str:name>/", views.EventCountryAPI.as_view(), name="event_country"),

	# Interests
	path("interests/new/", views.VolunteerInterestAPI.as_view(), name="volunteer_interest"),
	path("interests/delete/", views.VolunteerInterestAPI.as_view(), name="volunteer_interest"),
	path("interests/", views.VolunteerInterestAPI.as_view(), name="volunteer_interest"),
	path("interests/pk/<int:pk>/", views.VolunteerInterestAPI.as_view(), name="volunteer_interest"),
	# User Interests
	path("interests/user/new/", views.UserVolunteerInterestAPI.as_view(), name="user_volunteer_interest"),
	path("interests/user/delete/", views.UserVolunteerInterestAPI.as_view(), name="user_volunteer_interest"),
	path("interests/user/", views.UserVolunteerInterestAPI.as_view(), name="user_volunteer_interest"),
	path("interests/user/<int:user_id>/", views.UserVolunteerInterestAPI.as_view(), name="user_volunteer_interest"),
	path("interests/user/pk/<int:pk>/", views.UserVolunteerInterestAPI.as_view(), name="user_volunteer_interest"),
	# Skills
	path("skills/new/", views.VolunteerSkillAPI.as_view(), name="volunteer_skill"),
	path("skills/delete/", views.VolunteerSkillAPI.as_view(), name="volunteer_skill"),
	path("skills/", views.VolunteerSkillAPI.as_view(), name="volunteer_skill"),
	path("skills/pk/<int:pk>/", views.VolunteerSkillAPI.as_view(), name="volunteer_skill"),
	
	# User Skills
	path("skills/user/new/", views.UserVolunteerSkillAPI.as_view(), name="user_volunteer_skill"),
	path("skills/user/delete/", views.UserVolunteerSkillAPI.as_view(), name="user_volunteer_skill"),
	path("skills/user/", views.UserVolunteerSkillAPI.as_view(), name="user_volunteer_skill"),
	path("skills/user/<int:user_id>/", views.UserVolunteerSkillAPI.as_view(), name="user_volunteer_skill"),
	path("skills/user/pk/<int:pk>/", views.UserVolunteerSkillAPI.as_view(), name="user_volunteer_skill"),

	# Events1
	path("volunteer_event/new/", views.VolunteerEventAPI.as_view(), name="vol_event"),
	path("volunteer_event/delete/", views.VolunteerEventAPI.as_view(), name="vol_event"),
	path("volunteer_event/pk/<int:pk>/", views.VolunteerEventAPI.as_view(), name="get_vol_event"),
	path("volunteer_event/state/<int:state>/", views.VolunteerEventAPI.as_view(), name="get_vol_event"),
	path("volunteer_event/city/<int:city>/", views.VolunteerEventAPI.as_view(), name="get_vol_event"),
	path("volunteer_event/provider/<int:provider>/", views.VolunteerEventAPI.as_view(), name="get_vol_event"),
	path("volunteer_event/tag/<str:tags>/", views.VolunteerEventAPI.as_view(), name="get_vol_event"),
	# Posts
	path("volunteer_post/new/", views.VolunteerPostAPI.as_view(), name="vol_post"),
	path("volunteer_post/delete/", views.VolunteerPostAPI.as_view(), name="vol_post"),
	path("volunteer_post/user/<int:user_id>/", views.VolunteerPostAPI.as_view(), name="get_vol_post"),
	path("volunteer_post/event/<int:event_id>/", views.VolunteerPostAPI.as_view(), name="get_vol_post"),
	# Signups
	path("volunteer_event_signup/new/", views.VolunteerEventSignUpAPI.as_view(), name="volunteer_event_signup"),
	path("volunteer_event_signup/delete/", views.VolunteerEventSignUpAPI.as_view(), name="volunteer_event_signup"),
	path("volunteer_event_signup/pk/<int:pk>/", views.VolunteerEventSignUpAPI.as_view(), name="get_volunteer_event_signup"),
	path("volunteer_event_signup/volunteer/<int:volunteer_id>/", views.VolunteerEventSignUpAPI.as_view(), name="get_volunteer_event_signup"),
	path("volunteer_event_signup/event/<int:event_id>/", views.VolunteerEventSignUpAPI.as_view(), name="get_volunteer_event_signup"),

	path("donation_event/new/", views.DonationEventAPI.as_view(), name="donation_event"),
	path("donation_event/delete/", views.DonationEventAPI.as_view(), name="donation_event_delete"),
	path("donation_event/", views.DonationEventAPI.as_view(), name="get_donation_event"),
	path("donation_event/pk/<int:pk>/", views.DonationEventAPI.as_view(), name="get_donation_event"),
	path("donation_event/<str:field>/<str:query>/", views.DonationEventAPI.as_view(), name="get_donation_event"),

	path("make_donation/", views.DonationAPI.as_view(), name="make_donation"),
	path("user_donation/user/<int:user_id>/", views.DonationAPI.as_view(), name="get_donation"),
	path("user_donation/event/<int:event_id>/", views.DonationAPI.as_view(), name="get_donation"),
	path("user_donation/charge/<str:charge_id>/", views.DonationAPI.as_view(), name="get_donation"),
	
	path("refund_user_donation/", views.DonationAPI.as_view(), name="delete_donation"),
	path("user_donation_refund/charge/live/<str:charge_id>/<int:live>/", views.UserDonationRefundAPI.as_view(), name="get_refund"), # live 0 == False(Database), 1 == True(Stripe API)
	path("user_donation_refund/refund/live/<str:refund_id>/<int:live>/", views.UserDonationRefundAPI.as_view(), name="get_refund"),
	path("user_donation_refund/charge/<str:charge_id>/", views.UserDonationRefundAPI.as_view(), name="get_refund"),
	path("user_donation_refund/refund/<str:refund_id>/", views.UserDonationRefundAPI.as_view(), name="get_refund"),
	# News API
	path("news/city/state/<str:city>/<str:state>/<str:keyword>/", views.NewsAPI.as_view(), name="news_api"),
	path("news/state/<str:state>/<str:keyword>/", views.NewsAPI.as_view(), name="news_api")


] 