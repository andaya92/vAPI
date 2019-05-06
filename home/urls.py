from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "home"
 
urlpatterns = [
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
	# Events
	path("volunteer_event/new/", views.VolunteerEventAPI.as_view(), name="vol_event"),
	path("volunteer_event/delete/", views.VolunteerEventAPI.as_view(), name="vol_event"),
	path("volunteer_event/pk/<int:pk>/", views.VolunteerEventAPI.as_view(), name="get_vol_event"),
	path("volunteer_event/state/<int:state>/", views.VolunteerEventAPI.as_view(), name="get_vol_event"),
	path("volunteer_event/city/<int:city>/", views.VolunteerEventAPI.as_view(), name="get_vol_event"),
	path("volunteer_event/provider/<int:provider>/", views.VolunteerEventAPI.as_view(), name="get_vol_event"),
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

	path("donation_event/", views.DonationEventAPI.as_view(), name="donation_event"),
	path("donation_event/delete/", views.DonationEventAPI.as_view(), name="donation_event_delete"),
	path("donation_event/pk/<int:pk>/", views.DonationEventAPI.as_view(), name="get_donation_event"),
	path("donation_event/<str:field>/<str:query>/", views.DonationEventAPI.as_view(), name="get_donation_event"),

	path("make_donation/", views.DonationAPI.as_view(), name="make_donation"),
	path("user_donation/user/<int:user_id>/", views.DonationAPI.as_view(), name="get_donation"),
	path("user_donation/event/<int:event_id>/", views.DonationAPI.as_view(), name="get_donation"),
	path("user_donation/charge/<str:charge_id>/", views.DonationAPI.as_view(), name="get_donation"),
	path("refund_user_donation/", views.DonationAPI.as_view(), name="delete_donation")


] 