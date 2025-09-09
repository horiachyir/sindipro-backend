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
    buildingType = serializers.CharField(source='building_type', required=False)
    requiresQuote = serializers.BooleanField(source='requires_quote')
    dueMonth = serializers.CharField(source='due_month', required=False)
    responsibleEmails = serializers.CharField(source='responsible_emails', required=False)
    
    class Meta:
        model = LegalTemplate
        fields = [
            'id',
            'name',
            'description',
            'buildingType',
            'frequency',
            'conditions',
            'requiresQuote',
            'active',
            'dueMonth',
            'responsibleEmails',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)