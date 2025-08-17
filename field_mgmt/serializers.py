from rest_framework import serializers
from .models import FieldRequest, FieldMgmtTechnical, FieldMgmtTechnicalImage
from building_mgmt.models import Building
import base64
from django.core.files.base import ContentFile


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


class FieldMgmtTechnicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldMgmtTechnicalImage
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class FieldMgmtTechnicalSerializer(serializers.ModelSerializer):
    images = FieldMgmtTechnicalImageSerializer(many=True, read_only=True)
    image_data = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = FieldMgmtTechnical
        fields = ['id', 'company_email', 'title', 'description', 'location', 
                 'priority', 'images', 'image_data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'images']
    
    def create(self, validated_data):
        image_data_list = validated_data.pop('image_data', [])
        technical_request = FieldMgmtTechnical.objects.create(**validated_data)
        
        for image_data in image_data_list:
            if image_data.startswith('data:image'):
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'technical_{technical_request.id}_{len(technical_request.images.all())}.{ext}')
                FieldMgmtTechnicalImage.objects.create(
                    technical_request=technical_request,
                    image=data
                )
        
        return technical_request