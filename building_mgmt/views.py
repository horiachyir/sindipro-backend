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
    Get all buildings with only id and building_name fields.
    Accessible without authentication for frontend signup process.
    """
    buildings = Building.objects.all().only('id', 'building_name')
    serializer = BuildingBasicSerializer(buildings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_units(request):
    units = Unit.objects.filter(
        block__building__created_by=request.user
    ).select_related('block', 'block__building').order_by('block__building__building_name', 'block__name', 'number')
    
    serializer = UnitDetailSerializer(units, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_unit(request, tower_id):
    print(f"DEBUG: Received request for tower_id: {tower_id}")
    print(f"DEBUG: User: {request.user}")
    print(f"DEBUG: Request data: {request.data}")
    
    # Verify the tower exists and belongs to a building owned by the user
    try:
        tower = Tower.objects.select_related('building').get(id=tower_id, building__created_by=request.user)
        print(f"DEBUG: Found tower: {tower} in building: {tower.building}")
    except Tower.DoesNotExist:
        print(f"DEBUG: Tower {tower_id} not found or access denied for user {request.user}")
        return Response({
            'error': 'Tower not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Remove block_id from request data if present (since it comes from URL)
    data = request.data.copy()
    if 'block_id' in data:
        data.pop('block_id')
    
    serializer = UnitSerializer(data=data)
    
    if serializer.is_valid():
        # Set the block (tower) from the URL parameter
        unit = serializer.save(block=tower)
        return Response({
            'message': 'Unit created successfully',
            'unit': UnitSerializer(unit).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Invalid data',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)