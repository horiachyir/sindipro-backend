from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ConsumptionRegister, ConsumptionAccount
from .serializers import ConsumptionRegisterSerializer, ConsumptionAccountSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_consumption_register(request):
    """
    Create a new consumption register entry.
    Expected data: {date, gasCategory, utilityType, value}
    """
    serializer = ConsumptionRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_consumption_account(request):
    """
    Create a new consumption account entry.
    Expected data: {amount, month, paymentDate, utilityType}
    """
    serializer = ConsumptionAccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)