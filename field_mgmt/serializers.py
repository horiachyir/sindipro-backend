from rest_framework import serializers
from .models import FieldRequest
from building_mgmt.models import Building


class FieldRequestSerializer(serializers.ModelSerializer):
    building_id = serializers.PrimaryKeyRelatedField(
        queryset=Building.objects.all(), 
        source='building'
    )
    building_name = serializers.CharField(source='building.building_name', read_only=True)
    
    class Meta:
        model = FieldRequest
        fields = ['id', 'building_id', 'building_name', 'caretaker', 'title', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'building_name', 'created_at', 'updated_at']
    
    def validate_items(self, value):
        """Validate items structure"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Items must be a list")
        
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Each item must be an object")
            
            required_fields = ['observations', 'productType', 'quantity']
            for field in required_fields:
                if field not in item:
                    raise serializers.ValidationError(f"Item missing required field: {field}")
            
            if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be a positive integer")
        
        return value