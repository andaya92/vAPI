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






