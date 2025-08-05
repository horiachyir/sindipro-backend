from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Address(models.Model):
    cep = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    street = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.street}, {self.number}, {self.neighborhood}, {self.city}/{self.state}"

class Building(models.Model):
    BUILDING_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed', 'Mixed Use'),
    ]
    
    PHONE_TYPE_CHOICES = [
        ('mobile', 'Mobile'),
        ('landline', 'Landline'),
    ]
    
    # Basic Information
    building_name = models.CharField(max_length=200)
    building_type = models.CharField(max_length=20, choices=BUILDING_TYPE_CHOICES, default='residential')
    cnpj = models.CharField(max_length=18, unique=True)
    
    # Manager Information
    manager_name = models.CharField(max_length=200)
    manager_phone = models.CharField(max_length=30)
    manager_phone_type = models.CharField(max_length=20, choices=PHONE_TYPE_CHOICES, default='mobile')
    
    # Address Information
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='building_primary')
    use_separate_address = models.BooleanField(default=False)
    alternative_address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True, related_name='building_alternative')
    
    # Tower Information
    number_of_towers = models.PositiveIntegerField()
    
    # Residential-specific fields
    apartments_per_tower = models.PositiveIntegerField(null=True, blank=True)
    
    # Mixed-specific unit counts
    residential_units = models.PositiveIntegerField(null=True, blank=True)
    commercial_units = models.PositiveIntegerField(null=True, blank=True)
    non_residential_units = models.PositiveIntegerField(null=True, blank=True)
    studio_units = models.PositiveIntegerField(null=True, blank=True)
    wave_units = models.PositiveIntegerField(null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.building_name

class Tower(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='towers')
    name = models.CharField(max_length=100)
    units_per_tower = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.building.building_name} - {self.name}"

class TowerUnitDistribution(models.Model):
    tower = models.OneToOneField(Tower, on_delete=models.CASCADE, related_name='unit_distribution')
    commercial = models.PositiveIntegerField(default=0)
    non_residential = models.PositiveIntegerField(default=0)
    residential = models.PositiveIntegerField(default=0)
    studio = models.PositiveIntegerField(default=0)
    wave = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.tower.name} - Unit Distribution"

class Unit(models.Model):
    UNIT_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('store', 'Store'),
        ('parking', 'Parking Space'),
        ('storage', 'Storage'),
    ]
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=20)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES, default='apartment')
    floor = models.PositiveIntegerField()
    area_sqm = models.DecimalField(max_digits=8, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    
    # Owner Information
    owner_name = models.CharField(max_length=200)
    owner_cpf = models.CharField(max_length=14)
    owner_phone = models.CharField(max_length=20)
    owner_email = models.EmailField()
    
    # Financial Information
    common_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('building', 'unit_number')
    
    def __str__(self):
        return f"{self.building.name} - Unit {self.unit_number}"