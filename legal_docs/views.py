from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import LegalDocument, LegalObligation, LegalTemplate
from .serializers import LegalDocumentSerializer, LegalObligationSerializer, LegalTemplateSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_legal_template(request):
    serializer = LegalTemplateSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        template = serializer.save()
        return Response({
            'message': 'Legal template created successfully',
            'template_id': template.id,
            'template_name': template.name
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Invalid data',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)