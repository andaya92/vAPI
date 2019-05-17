from django.core.management.base import BaseCommand
from home.models import *



class Command(BaseCommand):

	def get_interests_skills(self):
		return ['Advocacy & Human Rights', 'Animals', 'Arts & Culture',
			'Board Development', 'Children & Youth', 'Community', 'Computers & Technology',
			'Crisis Support', 'Disaster Relief', 'Education & Literacy', 'Emergency & Safety', 
			'Employment', 'Environment', 'Faith-Based', 'Health & Medicine', 'Homeless & Housing', 'Hunger',
			'Immigrants & Refugees', 'International', ' Justice & Legal', 'LGBT', 'Media & Broadcasting',
			'People With Disabilities', 'Politics', 'Race & Ethnicity', 'Relief/Emergency', 'Seniors',
			'Sports & Recreation', 'Veterans & Military Families', 'Women'], ['Accounting', 'Event’s/Event Setup', 'Fundraising', 'Leadership', 'Manual Labor',
			'Organization', 'Problem Solving', 'Public Relations/Promotion', 'Report Writing',
			'Time Management', 'OR', 'Amiable', 'Analytical', 'Driver', 'Expressive']


	def handle(self, *args, **options):
		interests, skills = self.get_interests_skills()

		# try:
		for interest in interests:
			tmp = VolunteerInterest()
			tmp.name = interest
			tmp.save()


		for skill in skills:
			tmp = VolunteerSkill()
			tmp.name = skill
			tmp.save()
		# except:
		# 	print("failed")