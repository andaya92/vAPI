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
	email = models.EmailField(unique=True)
	def __str__(self):
		return "{} (PK:{}) {}".format(self.username, self.id, self.email)
	
	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def create_auth_token(sender, instance=None, created=False, **kwargs):
		if created:
			token = Token.objects.create(user=instance)
			instance.rest_token = token.key
			instance.save()

	


class Volunteer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return "{} (PK:{}) {}".format(self.user.username, self.id, self.user.email)

class VolunteerProvider(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return "{} (PK:{}) {}".format(self.user.username, self.id, self.user.email)

class EventState(models.Model):
	name = models.CharField(max_length=30, unique=True)

	def __str__(self):
		return "{} (PK:{})".format(self.name, self.id)

class EventCity(models.Model):
	name = models.CharField(max_length=50)
	state = models.ForeignKey(EventState, on_delete=models.CASCADE)
	
	def __str__(self):
		return "{} (PK:{}) {}".format(self.name, self.id, self.state.name)

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

	def __str__(self):
		return "{} (PK:{}) {}".format(self.provider.user.email, self.id, self.title)
	
class VolunteerEventSignUp(models.Model):
	volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
	event = models.ForeignKey(VolunteerEvent, on_delete=models.CASCADE)

	def __str__(self):
		return "{} (PK:{}) {}--{}".format(self.volunteer.user.email, self.id, self.event.title, self.event.provider.user.email)

	class Meta:
		unique_together = ('volunteer', 'event')

class VolunteerPost(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	event = models.ForeignKey(VolunteerEvent, on_delete=models.SET_NULL, null=True, blank=True)
	img = models.ImageField(upload_to="user_posts", default='empty_user_post.png')
	caption =models.CharField(max_length=480) #two tweets
	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField(editable=False)
	
	def __str__(self):
		return "{} (PK:{}) {}--{}".format(self.user.email, self.id, self.event.title, self.caption[:40])	

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(VolunteerPost, self).save(*args, **kwargs)

class DonationEvent(models.Model):
	title = models.CharField(max_length=100)
	desc = models.CharField(max_length=2000)
	details = models.CharField(max_length=500)
	beneficiary = models.CharField(max_length=100)

	def __str__(self):
		return "{} (PK:{}) {}--{}".format(self.title, self.id, self.desc[:20], self.beneficiary)

class UserDonation(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	event = models.ForeignKey(DonationEvent, on_delete=models.CASCADE)
	amount = models.FloatField()
	charge = models.CharField(max_length=50)

	def __str__(self):
		return "{} (PK:{}) {}--${}".format(self.user.email, self.id, self.event.title, self.amount)

class UserDonationRefund(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	event = models.ForeignKey(DonationEvent, on_delete=models.CASCADE)
	amount = models.FloatField()
	charge = models.CharField(max_length=50)
	refund = models.CharField(max_length=50)

	def __str__(self):
		return "{} (PK:{}) {}--${}".format(self.user.email, self.id, self.event.title, self.amount)