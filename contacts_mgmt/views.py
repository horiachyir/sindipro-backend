from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ContactsEvent
from .serializers import ContactsEventSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def event_handler(request):
    if request.method == 'GET':
        events = ContactsEvent.objects.all()
        serializer = ContactsEventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ContactsEventSerializer(data=request.data)
        
        if serializer.is_valid():
            event = serializer.save(created_by=request.user)
            return Response({
                'message': 'Event created successfully',
                'event': ContactsEventSerializer(event).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Invalid data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
