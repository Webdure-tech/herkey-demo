from django.db import models
from django.contrib.auth.models import User
from utils.model_abstract import Model
from django_extensions.db.models import (
	TimeStampedModel,
	ActivatorModel,
	TitleDescriptionModel
)

class Event(
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
	Model
	):

	class Meta:
		verbose_name_plural = "Events"

	# Define the choices for the type field
	TYPE_CHOICES = [
		('SCHEDULED', 'Scheduled'),
		('LIVE', 'Live'),
		('COMPLETED', 'Completed'),
	]

	type = models.CharField(
		max_length=10,
		choices=TYPE_CHOICES,
		default='SCHEDULED',
		verbose_name="Type"
	)

	# Add the scheduled_date field
	scheduled_date = models.DateTimeField(
		null=True,
		blank=True,
		verbose_name="Scheduled Date"
	)

	active = models.BooleanField(
		default=True,
		verbose_name="Active"
	)

	stream_session_id = models.CharField(
		null=True,
		blank=True,
		max_length=100,
		verbose_name="Stream Session ID"
	)

	def __str__(self):
		return f'{self.title}'
	

class EventParticipant(
	TimeStampedModel,
	Model
	):

	class Meta:
		verbose_name_plural = "Events_Participants"

	event = models.ForeignKey(
		Event,
		on_delete=models.CASCADE,
		related_name='participants',
		verbose_name="Event"
	)

	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='event_participants',
		verbose_name="User"
	)

	active = models.BooleanField(
		default=True,
		verbose_name="Active"
	)

	PARTICIPANT_TYPE = [
		('HOST', 'Host'),
		('PARTICIPANT', 'Participant'),
	]
	type = models.CharField(
		max_length=20,
		choices=PARTICIPANT_TYPE,
		default='PARTICIPANT',
		verbose_name="Type"
	)

	def __str__(self):
		return 'event_participants'
	

class EventAttachment(
	TimeStampedModel,
	Model
	):

	class Meta:
		verbose_name_plural = "Events_Attachments"
		constraints = [
			models.UniqueConstraint(
                fields=['event'],
                condition=models.Q(type='BANNER'),
                name='unique_event_banner'
            )
		]

	event = models.ForeignKey(
		Event,
		on_delete=models.CASCADE,
		related_name='attachments',
		verbose_name="Event"
	)

	attachment_cloud_id = models.CharField(
		null=True,
		max_length=100,
		verbose_name="Attachment"
	)

	attachment_name = models.CharField(
		null=True,
		max_length=100,
		verbose_name="Attachment Name"
	)

	ATTACHMENT_TYPE_CHOICES = [
		('BANNER', 'banner'),
		('EVENT_IMAGE', 'event_image'),
	]

	type = models.CharField(
		max_length=20,
		choices=ATTACHMENT_TYPE_CHOICES,
		default='EVENT_IMAGE',
		verbose_name="Type"
	)

	active = models.BooleanField(
		default=True,
		verbose_name="Active"
	)

	def __str__(self):
		return 'event_attachments'