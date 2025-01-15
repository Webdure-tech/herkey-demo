""" Serializers for the core app. """

import boto3
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        )


class EventParticipantsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.EventParticipant
        fields = (
            "id",
            "event",
            "event_id",
            "user",
            "user_id",
            "active",
            "type",
            "created",
            "modified",
        )


class EventAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventAttachment
        fields = (
            "id",
            "attachment_cloud_id",
            "event",
            "event_id",
            "type",
            "active",
            "created",
            "modified",
        )

    def create(self, validated_data):
        event_id = validated_data.pop("event_id")
        event = models.Event.objects.get(id=event_id)
        attachment = models.EventAttachment.objects.create(
            event=event, **validated_data
        )
        return attachment

    def get_signed_url(self, obj):
        """ "
        Generate a signed URL for the attachment."""
        if not obj.attachment_cloud_id:
            return None

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        try:
            signed_url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                    "Key": obj.attachment_cloud_id,
                },
                ExpiresIn=7200,  # URL expiration time in seconds
            )
            return signed_url
        except Exception as e:
            return str(e)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["signed_url"] = self.get_signed_url(instance)
        return representation


class EventSerializer(serializers.ModelSerializer):
    participants = EventParticipantsSerializer(many=True, read_only=True)
    attachments = EventAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Event
        fields = (
            "id",
            "title",
            "description",
            "type",
            "scheduled_date",
            "end_date",
            "created",
            "modified",
            "active",
            "stream_session_id",
            "participants",
            "attachments",
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return data
