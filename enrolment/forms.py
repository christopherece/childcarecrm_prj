from django import forms
from .models import Enrolment, ParentGuardian, MedicalInformation, EmergencyContact
from attendance.models import Child, Center, Room

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'date_of_birth', 'gender', 'emergency_contact', 'emergency_phone', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }


class EnrolmentForm(forms.ModelForm):
    class Meta:
        model = Enrolment
        fields = ['center', 'room', 'start_date', 'notes']
        widgets = {
            'center': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter rooms based on selected center
        self.fields['room'].queryset = Room.objects.none()
        
        if 'center' in self.data:
            try:
                center_id = int(self.data.get('center'))
                self.fields['room'].queryset = Room.objects.filter(center_id=center_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty room queryset
        elif self.instance.pk:
            self.fields['room'].queryset = Room.objects.filter(center=self.instance.center).order_by('name')

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
