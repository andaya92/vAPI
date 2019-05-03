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
