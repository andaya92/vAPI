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
	path("location/city/new/", views.EventCityAPI.as_view(), name="event_city"),
	path("location/city/delete/", views.EventCityAPI.as_view(), name="event_city"),
	path("location/city/", views.EventCityAPI.as_view(), name="event_city"),
	path("location/city/pk/<int:pk>/", views.EventCityAPI.as_view(), name="event_city"),
	path("location/city/<str:name>/", views.EventCityAPI.as_view(), name="event_city"),
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






