from django.contrib import admin
from .models import Enrolment, ParentGuardian, MedicalInformation, EmergencyContact

@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    list_display = ('child', 'status', 'start_date', 'enrolment_date', 'notes')
    list_filter = ('status', 'start_date', 'enrolment_date')
    search_fields = ('child__name', 'notes')
    ordering = ('-enrolment_date',)
    readonly_fields = ('enrolment_date',)

@admin.register(ParentGuardian)
class ParentGuardianAdmin(admin.ModelAdmin):
    list_display = ('child', 'full_name', 'relationship', 'email', 'phone_number', 'emergency_contact')
    list_filter = ('relationship', 'emergency_contact')
    search_fields = ('child__name', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('child__name', 'last_name', 'first_name')
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

@admin.register(MedicalInformation)
class MedicalInformationAdmin(admin.ModelAdmin):
    list_display = ('child', 'has_allergies', 'has_medical_conditions', 'has_medications')
    search_fields = ('child__name', 'allergies', 'medical_conditions', 'medications')
    ordering = ('child__name',)
    
    def has_allergies(self, obj):
        return bool(obj.allergies)
    has_allergies.boolean = True
    has_allergies.short_description = 'Allergies'
    
    def has_medical_conditions(self, obj):
        return bool(obj.medical_conditions)
    has_medical_conditions.boolean = True
    has_medical_conditions.short_description = 'Medical Conditions'
    
    def has_medications(self, obj):
        return bool(obj.medications)
    has_medications.boolean = True
    has_medications.short_description = 'Medications'

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('child', 'full_name', 'relationship', 'phone_number', 'can_pickup')
    list_filter = ('relationship', 'can_pickup')
    search_fields = ('child__name', 'first_name', 'last_name', 'phone_number')
    ordering = ('child__name', 'last_name', 'first_name')
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
