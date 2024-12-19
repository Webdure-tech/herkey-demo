""" Views for the core app. """

from json import JSONDecodeError
from uuid import UUID, uuid4
import boto3


from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .agora import create_agora_rtc_token_publisher
from .models import Event, EventParticipant, EventAttachment
from .serializers import (
    EventSerializer,
    EventParticipantsSerializer,
    EventAttachmentSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer
)



class EventViewSet(viewsets.ViewSet):
    """
    A simple APIView for creating event entires.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        """"
        Extra context provided to the serializer class."""
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and"""
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def create(self, request):
        """"
        Create a new event entry."""
        try:
            data = JSONParser().parse(request)
            serializer = EventSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
        
    def update(self, request, pk=None):
        """"
        Update an existing event entry."""
        try:
            if not isinstance(pk, UUID):
                pk = UUID(pk)
            data = JSONParser().parse(request)
            event = Event.objects.get(id=pk)
            serializer = EventSerializer(event, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
        
    def list(self, request):
        """"
        Return all event entries."""
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Retrieve a single event entry by ID."""
        if not isinstance(pk, UUID):
            pk = UUID(pk)
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def destroy(self, request):
        """"
        Delete an existing event entry."""
        try:
            data = JSONParser().parse(request)
            event = Event.objects.get(id=data['id'])
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

    @action(detail=True, methods=['post'])
    def participants(self, request, pk=None):
        """Add a participant to an event."""
        event = get_object_or_404(Event, pk=pk)
        data = JSONParser().parse(request)
        serializer = EventParticipantsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def get_participants(self, request, pk=None):
        """Get all participants of an event."""
        event = get_object_or_404(Event, pk=pk)
        participants = event.participants.all()
        serializer = EventParticipantsSerializer(participants, many=True)
        return Response(serializer.data)


class EventParticipantViewSet(viewsets.ViewSet):
    """
    A simple APIView for creating event participant entires.
    """
    serializer_class = EventParticipantsSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        """"
        Extra context provided to the serializer class."""
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and"""
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def create(self, request):
        """"
        Create a new event participant entry."""
        try:
            data = JSONParser().parse(request)
            username = request.user.username
            user = get_object_or_404(User, username=username)
            event_id = data.get('event')
            event = get_object_or_404(Event, id=event_id)
            serializer = EventParticipantsSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, event=event)
                return Response(serializer.data)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
    
    def delete(self, request):
        """"
        Delete an existing event participant entry."""
        try:
            data = JSONParser().parse(request)
            event_participant = EventParticipant.objects.get(id=data['id'])
            event_participant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
        

class EventAttachmentViewSet(viewsets.ViewSet):
    """
    A simple APIView for adding event attachment entires.
    """
    serializer_class = EventAttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        """"
        Extra context provided to the serializer class."""
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and"""
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def create(self, request):
        """"
        Create a new event participant entry."""
        try:
            data = JSONParser().parse(request)
            serializer = EventAttachmentSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
    
    def delete(self, request):
        """"
        Delete an existing event attachment entry."""
        try:
            data = JSONParser().parse(request)
            event_attachment = EventAttachment.objects.get(id=data['id'])
            event_attachment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
    
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_pre_signed_url(request):
    """Get a pre-signed URL for an attachment."""
    data = JSONParser().parse(request)
    file_name = data.get('file_name')
    file_name_without_extension = file_name.split('.')[0]
    if not file_name:
        return Response({"error": "attachment_cloud_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    cloud_id = f'event_attachments/{file_name_without_extension}_{uuid4()}'
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    fields=None
    conditions=None
    try:
        signed_url = s3_client.generate_presigned_post(
            settings.AWS_STORAGE_BUCKET_NAME,
            cloud_id,
            Fields=fields,
             Conditions=conditions,
            ExpiresIn=3600  # URL expiration time in seconds
        )
        return Response({"signed_url": signed_url, "cloud_id": cloud_id})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_agora_token(request):
    """Create an Agora RTC token for a publisher."""
    data = JSONParser().parse(request)
    username = request.user
    channel_name = data.get('event_id')
    event = get_object_or_404(Event, id=channel_name)
    user = get_object_or_404(User, username=username)
    serializer = UserSerializer(user)
    event_participant = get_object_or_404(EventParticipant, event=event, user=user)
    role = 'host' if event_participant.type == "HOST" else 'audience'
    user_id = serializer.data.get('id')
    token = create_agora_rtc_token_publisher(channel_name, user_id, role)
    return Response(token)

@api_view(['GET'])
def health_check(request):
    return JsonResponse({"status": "healthy"})