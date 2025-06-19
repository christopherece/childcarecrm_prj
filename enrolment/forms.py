from django import forms
from .models import Enrolment, ParentGuardian, MedicalInformation, EmergencyContact
from attendance.models import Child

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'date_of_birth', 'gender', 'emergency_contact', 'emergency_phone', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

from attendance.models import Center

class EnrolmentForm(forms.ModelForm):
    center = forms.ModelChoiceField(
        queryset=Center.objects.all(),
        empty_label="Select a Childcare Center",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Enrolment
        fields = ['center', 'start_date', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class ParentGuardianForm(forms.ModelForm):
    class Meta:
        model = ParentGuardian
        fields = ['relationship', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'emergency_contact']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class MedicalInformationForm(forms.ModelForm):
    class Meta:
        model = MedicalInformation
        fields = ['allergies', 'medical_conditions', 'medications', 'medical_notes', 'immunization_record']
        widgets = {
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
            'medications': forms.Textarea(attrs={'rows': 3}),
            'medical_notes': forms.Textarea(attrs={'rows': 3}),
        }

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['first_name', 'last_name', 'relationship', 'phone_number', 'address', 'can_pickup']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
