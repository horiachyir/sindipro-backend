from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import FinancialMainAccount, AnnualBudget, Expense
from .serializers import FinancialMainAccountSerializer, FinancialMainAccountReadSerializer, AnnualBudgetSerializer, ExpenseSerializer

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def annual_budget_view(request):
    """
    POST: Create a new annual budget entry
    Expected data structure:
    {
        "account_category": "maintenance",
        "budgeted_amount": 5,
        "building_id": 1,
        "sub_item": "aaa"
    }
    """
    serializer = AnnualBudgetSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        annual_budget = serializer.save()
        return Response({
            'message': 'Annual budget created successfully',
            'budget_id': annual_budget.id,
            'category': annual_budget.category.name,
            'sub_item': annual_budget.sub_item,
            'budgeted_amount': str(annual_budget.budgeted_amount),
            'year': annual_budget.year
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Invalid data',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def expense_view(request):
    """
    POST: Create a new expense entry
    Expected data structure:
    {
        "amount": 7,
        "buildingId": "1",
        "category": "maintenance",
        "month": "2025-10"
    }
    """
    serializer = ExpenseSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        expense = serializer.save()
        return Response({
            'message': 'Expense created successfully',
            'expense_id': expense.id,
            'category': expense.category.name,
            'amount': str(expense.amount),
            'expense_date': expense.expense_date.strftime('%Y-%m-%d'),
            'building_id': expense.building_id
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Invalid data',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)