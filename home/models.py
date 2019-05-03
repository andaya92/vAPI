from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token

from vAPI import settings
import datetime
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
	photo = models.ImageField(upload_to="user_images", default='default_user.jpeg')
	DOB = models.DateField(default = datetime.date.today)
	rest_token = models.CharField(max_length=100, blank=True, null =True, unique=True)
	stripe_token = models.CharField(max_length=30, blank=True, null =True, unique=True)
	stripe_email = models.EmailField(blank=True, null =True, unique=True)
	customer_id = models.CharField(max_length=30, blank=True, null =True, unique=True) # Stripe CusId
	
	def __str__(self):
		return "{} (PK:{})".format(self.username, self.id)
	
	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def create_auth_token(sender, instance=None, created=False, **kwargs):
		if created:
			token = Token.objects.create(user=instance)
			instance.rest_token = token.key
			instance.save()

	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def create_superuser_password(sender, instance=None, created=False, **kwargs):
		if created:
			if instance.is_superuser:
				instance.set_password("temptemp!1")
				instance.save()

class Volunteer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

class VolunteerProvider(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

class EventState(models.Model):
	name = models.CharField(max_length=30, unique=True)

class EventCity(models.Model):
	name = models.CharField(max_length=50)
	state = models.ForeignKey(EventState, on_delete=models.CASCADE)
	class Meta:
		unique_together = ('name', 'state')

class VolunteerEvent(models.Model):
	title = models.CharField(max_length=100)
	location_city = models.ForeignKey(EventCity, on_delete=models.CASCADE)
	location_state = models.ForeignKey(EventState, on_delete=models.CASCADE)
	desc = models.CharField(max_length=2000)
	details = models.CharField(max_length=500)
	provider = models.ForeignKey(VolunteerProvider, on_delete=models.CASCADE)
	event_begins = models.DateTimeField()
	event_ends = models.DateTimeField()
	
class VolunteerEventSignUp(models.Model):
	volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
	event = models.ForeignKey(VolunteerEvent, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('volunteer', 'event')

class VolunteerPost(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	event = models.ForeignKey(VolunteerEvent, on_delete=models.SET_NULL, null=True, blank=True)
	img = models.ImageField(upload_to="user_posts", default='empty_user_post.png')
	caption =models.CharField(max_length=480) #two tweets
	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField()
	
	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(VolunteerPost, self).save(*args, **kwargs)
