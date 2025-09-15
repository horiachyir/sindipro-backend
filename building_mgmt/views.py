from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Building, Tower, Unit
from .serializers import BuildingSerializer, BuildingReadSerializer, UnitSerializer, UnitDetailSerializer, BuildingBasicSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_buildings(request):
    if request.method == 'GET':
        buildings = Building.objects.filter(created_by=request.user).prefetch_related('address', 'alternative_address', 'towers__unit_distribution')
        serializer = BuildingReadSerializer(buildings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = BuildingSerializer(data=request.data)
        
        if serializer.is_valid():
            building = serializer.save(created_by=request.user)
            return Response({
                'message': 'Building created successfully',
                'building_id': building.id,
                'building_name': building.building_name
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Invalid data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_building(request):
    serializer = BuildingSerializer(data=request.data)
    
    if serializer.is_valid():
        building = serializer.save(created_by=request.user)
        return Response({
            'message': 'Building created successfully',
            'building_id': building.id,
            'building_name': building.building_name
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Invalid data',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_buildings(request):
    """
    Get all buildings with id, building_name, and address fields.
    Accessible without authentication for frontend signup process.
    """
    buildings = Building.objects.all().select_related('address', 'alternative_address')
    serializer = BuildingBasicSerializer(buildings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_units(request):
    units = Unit.objects.filter(
        building__created_by=request.user
    ).select_related('building').order_by('building__building_name', 'number')
    
    serializer = UnitDetailSerializer(units, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_unit(request, id):
    print(f"DEBUG: Received request for building_id: {id}")
    print(f"DEBUG: User: {request.user}")
    print(f"DEBUG: Request data: {request.data}")
    
    # Verify the building exists and belongs to the user
    try:
        building = Building.objects.get(id=id, created_by=request.user)
        print(f"DEBUG: Found building: {building}")
    except Building.DoesNotExist:
        print(f"DEBUG: Building {id} not found or access denied for user {request.user}")
        return Response({
            'error': 'Building not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Remove building_id from request data if present (since it comes from URL)
    data = request.data.copy()
    if 'building_id' in data:
        data.pop('building_id')
    
    serializer = UnitSerializer(data=data)
    
    if serializer.is_valid():
        # Set the building from the URL parameter
        unit = serializer.save(building=building)
        return Response({
            'message': 'Unit created successfully',
            'unit': UnitSerializer(unit).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Invalid data',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)