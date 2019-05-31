from django.core.management.base import BaseCommand
from home.models import *
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):

	def get_interests_skills(self):
		return ['Advocacy & Human Rights', 'Animals', 'Arts & Culture',
			'Board Development', 'Children & Youth', 'Community', 'Computers & Technology',
			'Crisis Support', 'Disaster Relief', 'Education & Literacy', 'Emergency & Safety', 
			'Employment', 'Environment', 'Faith-Based', 'Health & Medicine', 'Homeless & Housing', 'Hunger',
			'Immigrants & Refugees', 'International', ' Justice & Legal', 'LGBT', 'Media & Broadcasting',
			'People With Disabilities', 'Politics', 'Race & Ethnicity', 'Relief/Emergency', 'Seniors',
			'Sports & Recreation', 'Veterans & Military Families', 'Women'],['Accounting', 'Event’s/Event Setup', 'Fundraising', 'Leadership', 'Manual Labor',
			'Organization', 'Problem Solving', 'Public Relations/Promotion', 'Report Writing',
			'Time Management', 'Amiable', 'Analytical', 'Driver', 'Expressive']


	def populate_interests_skills(self):
		logger.info("populate")
		interests, skills = self.get_interests_skills()
		try:
			for interest in interests:
				tmp = VolunteerInterest()
				tmp.name = interest
				tmp.save()


			for skill in skills:
				tmp = VolunteerSkill()
				tmp.name = skill
				tmp.save()
		except:
			print("failed")

	def populate_city_state(self):
		countries = {
			"United States"	: {
				"AZ" : {
					"26587" : ["Tempe", "Winslow", "Flagstaff"] 
				},
				"CA" : {
					"95382" : ['Atwater', "Manteca", "Modesto", "Ripon", "Sacramento"]	
				}
			}
		}

		for country in countries.keys():
			tmp_country = EventCountry()
			tmp_country.name = country
			tmp_country.save()
			for state in countries[country].keys():
				tmp_state = EventState()
				tmp_state.name = state
				tmp_state.country = tmp_country
				tmp_state.save()
				for zipcode in countries[country][state].keys():
					tmp_zipcode = ZipCode()
					tmp_zipcode.zip_code = zipcode
					tmp_zipcode.state = tmp_state
					tmp_zipcode.save()
					for city in countries[country][state][zipcode]:
						tmp_city = EventCity()
						tmp_city.name = city
						tmp_city.state = tmp_state
						tmp_city.zip_code = tmp_zipcode
						tmp_city.save()

	def handle(self, *args, **options):
		self.populate_interests_skills()
		self.populate_city_state()