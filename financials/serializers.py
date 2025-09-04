from rest_framework import serializers
from .models import FinancialMainAccount, AnnualBudget, BudgetCategory
from building_mgmt.models import Building
from datetime import datetime

class BuildingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['id', 'building_name', 'building_type', 'cnpj']

class FinancialMainAccountSerializer(serializers.ModelSerializer):
    building_id = serializers.IntegerField()
    parentId = serializers.IntegerField(source='parent_id', required=False, allow_null=True)
    actualAmount = serializers.DecimalField(source='actual_amount', max_digits=12, decimal_places=2)
    expectedAmount = serializers.DecimalField(source='expected_amount', max_digits=12, decimal_places=2)
    
    class Meta:
        model = FinancialMainAccount
        fields = ['building_id', 'code', 'name', 'type', 'parentId', 'actualAmount', 'expectedAmount']
        
    def create(self, validated_data):
        return FinancialMainAccount.objects.create(**validated_data)

class FinancialMainAccountReadSerializer(serializers.ModelSerializer):
    building = BuildingInfoSerializer(read_only=True)
    parentId = serializers.IntegerField(source='parent_id', read_only=True)
    actualAmount = serializers.DecimalField(source='actual_amount', max_digits=12, decimal_places=2, read_only=True)
    expectedAmount = serializers.DecimalField(source='expected_amount', max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = FinancialMainAccount
        fields = ['id', 'building', 'code', 'name', 'type', 'parentId', 'actualAmount', 'expectedAmount', 'created_at', 'updated_at']

class AnnualBudgetSerializer(serializers.ModelSerializer):
    account_category = serializers.CharField(write_only=True)
    building_id = serializers.IntegerField()
    sub_item = serializers.CharField(max_length=200)
    budgeted_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        model = AnnualBudget
        fields = ['account_category', 'building_id', 'sub_item', 'budgeted_amount']
        
    def create(self, validated_data):
        account_category_name = validated_data.pop('account_category')
        
        category, created = BudgetCategory.objects.get_or_create(
            name=account_category_name,
            defaults={'description': f'Category for {account_category_name}'}
        )
        
        current_year = datetime.now().year
        
        annual_budget = AnnualBudget.objects.create(
            building_id=validated_data['building_id'],
            year=current_year,
            category=category,
            sub_item=validated_data['sub_item'],
            budgeted_amount=validated_data['budgeted_amount'],
            created_by=self.context.get('request').user if self.context.get('request') else None
        )
        
        return annual_budget