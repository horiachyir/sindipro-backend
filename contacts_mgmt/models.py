from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactsEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('meetingEvent', 'Meeting Event'),
        ('generalEvent', 'General Event'),
        ('maintenanceEvent', 'Maintenance Event'),
        ('emergencyEvent', 'Emergency Event'),
    ]
    
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    date_time = models.DateTimeField()
    condominium = models.CharField(max_length=255)
    people_involved = models.JSONField(default=list)
    comments = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.event_type} ({self.date_time})"
    
    class Meta:
        db_table = 'contacts_mgmt_event'
        ordering = ['-date_time']
