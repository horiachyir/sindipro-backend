from rest_framework import serializers
from .models import LegalDocument, LegalObligation, LegalTemplate


class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')


class LegalObligationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalObligation
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')


class LegalTemplateSerializer(serializers.ModelSerializer):
    buildingTypes = serializers.ListField(
        child=serializers.CharField(),
        source='building_types',
        required=True
    )
    daysBeforeExpiry = serializers.IntegerField(source='days_before_expiry')
    requiresQuote = serializers.BooleanField(source='requires_quote')
    
    class Meta:
        model = LegalTemplate
        fields = [
            'id',
            'name',
            'description',
            'buildingTypes',
            'frequency',
            'conditions',
            'daysBeforeExpiry',
            'requiresQuote',
            'active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)