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
import openpyxl
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_units_excel(request, id):
    try:
        building = Building.objects.get(id=id, created_by=request.user)
    except Building.DoesNotExist:
        return Response({
            'error': 'Building not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)

    # Check if file was uploaded
    if 'file' not in request.FILES:
        return Response({
            'error': 'No file uploaded. Please upload an Excel file.'
        }, status=status.HTTP_400_BAD_REQUEST)

    excel_file = request.FILES['file']

    # Validate file type
    if not excel_file.name.endswith(('.xlsx', '.xls')):
        return Response({
            'error': 'Invalid file type. Please upload an Excel file (.xlsx or .xls).'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Load workbook
        wb = Workbook()
        try:
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
        except Exception as e:
            return Response({
                'error': f'Error reading Excel file: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Find header row (should be row 4 based on export format)
        header_row = 4
        headers = []
        for col in range(1, 13):  # 12 columns expected
            cell_value = ws.cell(row=header_row, column=col).value
            if cell_value:
                headers.append(str(cell_value).strip())
            else:
                headers.append("")

        # Expected headers from export
        expected_headers = [
            'Unit Number', 'Tower', 'Floor', 'Identification', 'Area (m²)',
            'Ideal Fraction', 'Status', 'Owner', 'Owner Phone', 'Parking Spaces',
            'Key Delivery', 'Deposit Location'
        ]

        # Validate headers
        if len(headers) < len(expected_headers):
            return Response({
                'error': 'Invalid Excel format. Missing required columns.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if headers match (allowing for some flexibility)
        header_matches = True
        for i, expected in enumerate(expected_headers):
            if i < len(headers) and expected.lower() not in headers[i].lower():
                header_matches = False
                break

        if not header_matches:
            return Response({
                'error': 'Invalid Excel format. Column headers do not match expected format.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Parse data rows (starting from row 5)
        units_data = []
        errors = []
        row_num = 5

        # Get all towers for this building to map tower names to IDs
        towers = {tower.name: tower for tower in building.towers.all()}

        # Create reverse mappings for choices
        status_map = {v: k for k, v in Unit.STATUS_CHOICES}
        identification_map = {v: k for k, v in Unit.IDENTIFICATION_CHOICES}

        while True:
            # Check if row has data (check first column)
            unit_number = ws.cell(row=row_num, column=1).value
            if not unit_number or str(unit_number).strip() == '':
                break

            try:
                # Extract all cell values
                row_data = []
                for col in range(1, 13):
                    cell_value = ws.cell(row=row_num, column=col).value
                    row_data.append(cell_value)

                # Parse and validate each field
                unit_number = str(row_data[0]).strip()
                tower_name = str(row_data[1]).strip() if row_data[1] else None
                floor = int(row_data[2]) if row_data[2] else 1
                identification_display = str(row_data[3]).strip() if row_data[3] else 'Residential'
                area = float(row_data[4]) if row_data[4] else 0.0
                ideal_fraction = float(row_data[5]) if row_data[5] else 0.0
                status_display = str(row_data[6]).strip() if row_data[6] else 'Vacant'
                owner = str(row_data[7]).strip() if row_data[7] else ''
                owner_phone = str(row_data[8]).strip() if row_data[8] else ''
                parking_spaces = int(row_data[9]) if row_data[9] else 0
                key_delivery = str(row_data[10]).strip() if row_data[10] else 'No'
                deposit_location = str(row_data[11]).strip() if row_data[11] else ''

                # Map display values back to database values
                status = status_map.get(status_display, 'vacant')
                identification = identification_map.get(identification_display, 'residential')

                # Find tower by name
                tower = None
                if tower_name and tower_name != 'N/A':
                    tower = towers.get(tower_name)
                    if not tower:
                        errors.append(f"Row {row_num}: Tower '{tower_name}' not found")
                        row_num += 1
                        continue

                # Validate required fields
                if not unit_number:
                    errors.append(f"Row {row_num}: Unit number is required")
                    row_num += 1
                    continue

                if area <= 0:
                    errors.append(f"Row {row_num}: Area must be greater than 0")
                    row_num += 1
                    continue

                # Create unit data
                unit_data = {
                    'building': building,
                    'tower': tower,
                    'number': unit_number,
                    'floor': floor,
                    'area': area,
                    'ideal_fraction': ideal_fraction,
                    'identification': identification,
                    'deposit_location': deposit_location,
                    'key_delivery': key_delivery,
                    'owner': owner,
                    'owner_phone': owner_phone,
                    'parking_spaces': parking_spaces,
                    'status': status,
                }

                units_data.append(unit_data)

            except (ValueError, TypeError) as e:
                errors.append(f"Row {row_num}: Invalid data format - {str(e)}")

            row_num += 1

        # If there are validation errors, return them
        if errors:
            return Response({
                'error': 'Data validation failed',
                'details': errors
            }, status=status.HTTP_400_BAD_REQUEST)

        if not units_data:
            return Response({
                'error': 'No valid unit data found in the Excel file'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Save units to database
        created_units = []
        update_count = 0
        create_count = 0

        for unit_data in units_data:
            try:
                # Check if unit already exists (by building and number)
                existing_unit = Unit.objects.filter(
                    building=building,
                    number=unit_data['number']
                ).first()

                if existing_unit:
                    # Update existing unit
                    for field, value in unit_data.items():
                        if field != 'building':  # Don't update building
                            setattr(existing_unit, field, value)
                    existing_unit.save()
                    created_units.append(existing_unit)
                    update_count += 1
                else:
                    # Create new unit
                    unit = Unit.objects.create(**unit_data)
                    created_units.append(unit)
                    create_count += 1

            except Exception as e:
                errors.append(f"Error saving unit {unit_data['number']}: {str(e)}")

        # If there were save errors, return them
        if errors:
            return Response({
                'error': 'Some units could not be saved',
                'details': errors,
                'partial_success': {
                    'created': create_count,
                    'updated': update_count
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Return success response with saved units
        serializer = UnitDetailSerializer(created_units, many=True)
        return Response({
            'message': f'Successfully imported {len(created_units)} units',
            'summary': {
                'total_processed': len(created_units),
                'created': create_count,
                'updated': update_count
            },
            'units': serializer.data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'error': f'Error processing Excel file: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)