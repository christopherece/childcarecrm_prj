from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Enrolment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    child = models.OneToOneField(
        'attendance.Child',
        on_delete=models.CASCADE,
        related_name='enrolment'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    enrolment_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Enrolment for {self.child.name}"

class ParentGuardian(models.Model):
    child = models.ForeignKey(
        'attendance.Child',
        on_delete=models.CASCADE,
        related_name='parent_guardians'
    )
    relationship = models.CharField(
        max_length=50,
        choices=[
            ('parent', 'Parent'),
            ('guardian', 'Guardian'),
            ('other', 'Other')
        ]
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField()
    emergency_contact = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.relationship} of {self.child.name}"

class MedicalInformation(models.Model):
    child = models.OneToOneField(
        'attendance.Child',
        on_delete=models.CASCADE,
        related_name='medical_info'
    )
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    medical_notes = models.TextField(blank=True)
    immunization_record = models.FileField(upload_to='immunization_records/', blank=True, null=True)

    def __str__(self):
        return f"Medical Info for {self.child.name}"

class EmergencyContact(models.Model):
    child = models.ForeignKey(
        'attendance.Child',
        on_delete=models.CASCADE,
        related_name='emergency_contacts'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField()
    can_pickup = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Emergency Contact for {self.child.name}"
