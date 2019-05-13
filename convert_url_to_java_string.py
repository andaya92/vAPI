import re

# Rules:
# 	1. path(url, view, name) must include spaces after each comma, especially url param
#	2. all query params must be at end of url endpoint 
		# /home/user/email/username/<str:email>/<str:username>/
		# 	name => home_user_email_username  
		# 	url => /home/user/email/username/
		# build in java with::
			# String user_email_lookup = home_user_email_username + "C@g.com/candaya/";

path_p = re.compile('path\("[a-zA-Z/]+\)"')
line_p = re.compile('path\\([\\S]*') # must contain a space after comma of path url

app_name = "home"

urls = '''
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

	path("donation_event/new/", views.DonationEventAPI.as_view(), name="donation_event"),
	path("donation_event/delete/", views.DonationEventAPI.as_view(), name="donation_event_delete"),
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
'''


# path("models/", views.index.as_view(), name="index"),

lines = line_p.findall(urls)
for line in lines:
	url = line[len('path("'):-2]

	pos = url.find("<")
	name = ""
	if pos != -1:
		url = url[:pos]
	name = url[:-1].replace("/", "_")

	print('public static final String {} = "{}/{}";'.format(name.upper(), app_name, url))





