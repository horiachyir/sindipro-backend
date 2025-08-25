from rest_framework import serializers
from .models import FinancialMainAccount

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