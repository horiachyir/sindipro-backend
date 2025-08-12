from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FieldRequest
from .serializers import FieldRequestSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def field_requests(request):
    """
    GET: Retrieve all field requests.
    POST: Create a new field request.
    Expected POST data: {building, caretaker, title, items}
    """
    if request.method == 'GET':
        requests = FieldRequest.objects.all()
        serializer = FieldRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = FieldRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)