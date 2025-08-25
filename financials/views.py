from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import FinancialMainAccount
from .serializers import FinancialMainAccountSerializer, FinancialMainAccountReadSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def financial_account_view(request):
    """
    GET: Retrieve all financial main accounts with building information
    POST: Create a new financial main account
    """
    if request.method == 'GET':
        accounts = FinancialMainAccount.objects.select_related('building').all()
        serializer = FinancialMainAccountReadSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
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