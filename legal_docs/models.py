from django.db import models
from django.contrib.auth import get_user_model
from building_mgmt.models import Building

User = get_user_model()

class LegalDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('statute', 'Building Statute'),
        ('regulation', 'Internal Regulation'),
        ('contract', 'Service Contract'),
        ('insurance', 'Insurance Policy'),
        ('license', 'Municipal License'),
        ('certificate', 'Certificate'),
        ('other', 'Other Document'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='legal_documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_number = models.CharField(max_length=100, blank=True)
    issuing_authority = models.CharField(max_length=200, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    file_document = models.FileField(upload_to='legal_documents/', null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.building.name}"
    
    @property
    def is_expired(self):
        if self.expiry_date:
            from django.utils import timezone
            return self.expiry_date < timezone.now().date()
        return False

class LegalObligation(models.Model):
    OBLIGATION_TYPE_CHOICES = [
        ('fire_safety', 'Fire Safety'),
        ('elevator_inspection', 'Elevator Inspection'),
        ('electrical_inspection', 'Electrical Inspection'),
        ('water_quality', 'Water Quality Test'),
        ('building_inspection', 'Building Inspection'),
        ('insurance_renewal', 'Insurance Renewal'),
        ('tax_payment', 'Tax Payment'),
        ('other', 'Other Obligation'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='legal_obligations')
    obligation_type = models.CharField(max_length=30, choices=OBLIGATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    responsible_party = models.CharField(max_length=200)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_obligations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.building.name}"
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.due_date < timezone.now().date() and self.status != 'completed'


class LegalTemplate(models.Model):
    FREQUENCY_CHOICES = [
        ('one_time', 'One Time'),
        ('annual', 'Annual'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
    ]
    
    BUILDING_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed', 'Mixed Use'),
        ('industrial', 'Industrial'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    building_types = models.JSONField(default=list)  # List of building types
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='annual')
    conditions = models.TextField(blank=True)
    days_before_expiry = models.IntegerField(default=30)
    requires_quote = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name