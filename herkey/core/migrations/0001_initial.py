# Generated by Django 4.1.3 on 2024-12-15 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('type', models.CharField(choices=[('SCHEDULED', 'Scheduled'), ('LIVE', 'Live'), ('COMPLETED', 'Completed')], default='SCHEDULED', max_length=10, verbose_name='Type')),
                ('scheduled_date', models.DateTimeField(blank=True, null=True, verbose_name='Scheduled Date')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('stream_session_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Stream Session ID')),
            ],
            options={
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('type', models.CharField(choices=[('HOST', 'Host'), ('PARTICIPANT', 'Participant')], default='PARTICIPANT', max_length=20, verbose_name='Type')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='core.event', verbose_name='Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_participants', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Events_Participants',
            },
        ),
        migrations.CreateModel(
            name='EventAttachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('attachment_cloud_id', models.CharField(max_length=100, null=True, verbose_name='Attachment')),
                ('attachment_name', models.CharField(max_length=100, null=True, verbose_name='Attachment Name')),
                ('type', models.CharField(choices=[('BANNER', 'banner'), ('EVENT_IMAGE', 'event_image')], default='EVENT_IMAGE', max_length=20, verbose_name='Type')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='core.event', verbose_name='Event')),
            ],
            options={
                'verbose_name_plural': 'Events_Attachments',
            },
        ),
        migrations.AddConstraint(
            model_name='eventattachment',
            constraint=models.UniqueConstraint(condition=models.Q(('type', 'BANNER')), fields=('event',), name='unique_event_banner'),
        ),
    ]