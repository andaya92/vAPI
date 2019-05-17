from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(User)
admin.site.register(Volunteer)
admin.site.register(VolunteerProvider)
admin.site.register(VolunteerEvent)
admin.site.register(VolunteerPost)
admin.site.register(VolunteerEventSignUp)
admin.site.register(EventCity)
admin.site.register(EventState)

admin.site.register(DonationEvent)
admin.site.register(UserDonation)
admin.site.register(UserDonationRefund)

admin.site.register(VolunteerInterest)
admin.site.register(VolunteerSkill)

admin.site.register(UserVolunteerInterest)
admin.site.register(UserVolunteerSkill)
