from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Building, Tower, Unit
from .serializers import BuildingSerializer, BuildingReadSerializer, UnitSerializer, UnitDetailSerializer, BuildingBasicSerializer
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import io

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

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_building(request, id):
    try:
        building = Building.objects.get(id=id, created_by=request.user)
    except Building.DoesNotExist:
        return Response({
            'error': 'Building not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        # Store building name for response message
        building_name = building.building_name

        # Explicitly delete address records from building_mgmt_address table
        if building.address:
            building.address.delete()

        if building.alternative_address:
            building.alternative_address.delete()

        # Delete the building (this will cascade delete all related records including towers)
        building.delete()

        return Response({
            'message': f'Building "{building_name}" and all associated data have been successfully deleted'
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BuildingSerializer(building, data=request.data)

        if serializer.is_valid():
            updated_building = serializer.save()
            return Response({
                'message': 'Building updated successfully',
                'building_id': updated_building.id,
                'building_name': updated_building.building_name
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Invalid data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_buildings(request):
    """
    Get all buildings with all fields from building_mgmt_building, building_mgmt_address, and building_mgmt_tower tables.
    Accessible without authentication for frontend signup process.
    """
    buildings = Building.objects.all().select_related('address', 'alternative_address').prefetch_related('towers__unit_distribution')
    serializer = BuildingReadSerializer(buildings, many=True)
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

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_unit(request, id):
    try:
        unit = Unit.objects.get(id=id, building__created_by=request.user)
    except Unit.DoesNotExist:
        return Response({
            'error': 'Unit not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        # Store unit info for response message
        unit_number = unit.number
        building_name = unit.building.building_name

        # Delete the unit from building_mgmt_unit table
        unit.delete()

        return Response({
            'message': f'Unit {unit_number} from building "{building_name}" has been successfully deleted'
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UnitSerializer(unit, data=request.data)

        if serializer.is_valid():
            updated_unit = serializer.save()
            return Response({
                'message': 'Unit updated successfully',
                'unit': UnitDetailSerializer(updated_unit).data
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Invalid data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_units_excel(request, id):
    try:
        building = Building.objects.get(id=id, created_by=request.user)
    except Building.DoesNotExist:
        return Response({
            'error': 'Building not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)

    # Get all units for this building with related data
    units = Unit.objects.filter(building=building).select_related(
        'building', 'tower'
    ).order_by('tower__name', 'floor', 'number')

    # Create workbook and worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = f"{building.building_name} - Units Report"

    # Define styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    # Title and building information
    ws.merge_cells('A1:L1')
    title_cell = ws['A1']
    title_cell.value = f"Building Units Report - {building.building_name}"
    title_cell.font = Font(bold=True, size=16)
    title_cell.alignment = Alignment(horizontal="center")

    ws.merge_cells('A2:L2')
    building_info = ws['A2']
    address = building.address
    address_str = f"{address.street}, {address.number}, {address.neighborhood}, {address.city}/{address.state}"
    building_info.value = f"Address: {address_str} | CNPJ: {building.cnpj} | Manager: {building.manager_name}"
    building_info.alignment = Alignment(horizontal="center")

    # Headers
    headers = [
        'Unit Number', 'Tower', 'Floor', 'Identification', 'Area (m²)',
        'Ideal Fraction', 'Status', 'Owner', 'Owner Phone', 'Parking Spaces',
        'Key Delivery', 'Deposit Location'
    ]

    # Write headers
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border

    # Write unit data
    row = 5
    for unit in units:
        # Display names instead of IDs
        tower_name = unit.tower.name if unit.tower else "N/A"

        # Map status values to readable text
        status_display = dict(Unit.STATUS_CHOICES).get(unit.status, unit.status)

        # Map identification values to readable text
        identification_display = dict(Unit.IDENTIFICATION_CHOICES).get(unit.identification, unit.identification)

        data = [
            unit.number,
            tower_name,
            unit.floor,
            identification_display,
            float(unit.area),
            float(unit.ideal_fraction),
            status_display,
            unit.owner,
            unit.owner_phone,
            unit.parking_spaces,
            unit.key_delivery,
            unit.deposit_location or "N/A"
        ]

        for col, value in enumerate(data, 1):
            cell = ws.cell(row=row, column=col)
            cell.value = value
            cell.border = border
            # Center alignment for numeric and status fields
            if col in [3, 4, 5, 6, 7, 10]:  # Floor, identification, area, fraction, status, parking
                cell.alignment = Alignment(horizontal="center")

        row += 1

    # Auto-adjust column widths
    for col in range(1, len(headers) + 1):
        column_letter = get_column_letter(col)
        max_length = 0

        # Check header length
        max_length = max(max_length, len(str(headers[col-1])))

        # Check data lengths
        for row_num in range(5, row):
            cell_value = ws.cell(row=row_num, column=col).value
            if cell_value:
                max_length = max(max_length, len(str(cell_value)))

        # Set column width with some padding
        adjusted_width = min(max_length + 2, 50)  # Max width of 50
        ws.column_dimensions[column_letter].width = adjusted_width

    # Add summary information
    summary_row = row + 2
    ws.merge_cells(f'A{summary_row}:D{summary_row}')
    summary_cell = ws[f'A{summary_row}']
    summary_cell.value = f"Total Units: {units.count()}"
    summary_cell.font = Font(bold=True)

    # Status summary
    status_counts = {}
    for unit in units:
        status_display = dict(Unit.STATUS_CHOICES).get(unit.status, unit.status)
        status_counts[status_display] = status_counts.get(status_display, 0) + 1

    summary_row += 1
    for status_name, count in status_counts.items():
        ws.merge_cells(f'A{summary_row}:D{summary_row}')
        status_cell = ws[f'A{summary_row}']
        status_cell.value = f"{status_name}: {count} units"
        summary_row += 1

    # Create HTTP response
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    filename = f"{building.building_name.replace(' ', '_')}_units_report.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response