from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import FinancialMainAccount
from .serializers import FinancialMainAccountSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_financial_account(request):
    """
    Create a new financial main account
    """
    serializer = FinancialMainAccountSerializer(data=request.data)
    
    if serializer.is_valid():
        account = serializer.save()
        return Response({
            'message': 'Financial account created successfully',
            'account_id': account.id,
            'code': account.code,
            'name': account.name
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Invalid data',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)