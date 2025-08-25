from rest_framework import serializers
from .models import FinancialMainAccount
from building_mgmt.models import Building

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