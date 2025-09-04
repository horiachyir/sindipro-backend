# Building Seed Data for SINDIPRO Backend

## Problem Solved
The authentication system requires users to select a building during sign-in and sign-up, but the database had no building data, making registration impossible.

## Solution
Created a comprehensive seed data management command that populates the database with:
- 5 sample buildings (residential, commercial, and mixed types)
- 12 towers across all buildings
- 460 units with various configurations
- Complete address information for each building
- A demo user for testing

## Usage

### Running the Seed Command
```bash
# Activate virtual environment
source myenv/bin/activate

# Run the seed command
python manage.py seed_buildings
```

### Demo Credentials
After running the seed command, you can log in with:
- **Email**: demo@sindipro.com
- **Password**: demo123456
- **Building ID**: 1 (Edifício Copan) or any ID from 1-5

### Available Buildings
1. **Edifício Copan** (ID: 1)
   - Type: Residential
   - Location: São Paulo, SP
   - 1 tower, 120 units

2. **Torre Comercial Paulista** (ID: 2)
   - Type: Commercial
   - Location: Rio de Janeiro, RJ
   - 2 towers, 50 units total

3. **Condomínio Residencial Vista Verde** (ID: 3)
   - Type: Residential
   - Location: Belo Horizonte, MG
   - 3 towers, 120 units total

4. **Edifício Misto Central** (ID: 4)
   - Type: Mixed (residential/commercial)
   - Location: Curitiba, PR
   - 2 towers, 90 units total

5. **Residencial Park Plaza** (ID: 5)
   - Type: Residential
   - Location: São Paulo, SP
   - 4 towers, 120 units total

## Database Structure

### Building Model (`building_mgmt.models.Building`)
- Stores building information including name, type, CNPJ, manager details
- Links to Address model for location information
- Supports residential, commercial, and mixed-use buildings

### Tower Model (`building_mgmt.models.Tower`)
- Represents individual towers within a building
- Links to Building model via ForeignKey

### Unit Model (`building_mgmt.models.Unit`)
- Represents individual units (apartments/offices) within towers
- Includes details like floor, area, owner information, status

### User Model (`auth_system.models.User`)
- Extended Django User model with building association
- Users must be associated with a building for authentication

## Authentication Flow
1. User provides email, password, and building_id during login/registration
2. System validates credentials and building existence
3. User is associated with the selected building
4. JWT tokens are generated for authenticated sessions

## Notes
- The seed command is idempotent - running it multiple times won't create duplicates
- All created units have random but realistic data (area, floor, status, etc.)
- The demo user is created with 'manager' role for full system access
- Buildings have unique CNPJs to comply with Brazilian business requirements