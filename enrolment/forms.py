from django import forms
from django.core.validators import RegexValidator
from .models import Enrolment, ParentGuardian, MedicalInformation, EmergencyContact
from attendance.models import Child, Center, Room

class ChildForm(forms.ModelForm):
    emergency_phone = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be entered in the format: "+1234567890". Up to 15 digits allowed.'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'e.g. +64211234567'}),
        required=True
    )
    center = forms.ModelChoiceField(
        queryset=Center.objects.all(),
        empty_label="Select a center",
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    class Meta:
        model = Child
        fields = ['name', 'date_of_birth', 'gender', 'emergency_contact', 'emergency_phone', 'profile_picture', 'center']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +64211234567'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'center': forms.Select(attrs={'class': 'form-select'}),
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
    phone_number = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be entered in the format: "+1234567890". Up to 15 digits allowed.'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'e.g. +64211234567'}),
        required=True
    )

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
    phone_number = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be entered in the format: "+1234567890". Up to 15 digits allowed.'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +64211234567'}),
        required=True
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
        required=True
    )

    class Meta:
        model = EmergencyContact
        fields = ['first_name', 'last_name', 'relationship', 'phone_number', 'address', 'email', 'can_pickup']
        widgets = {
            'relationship': forms.Select(attrs={'class': 'form-select'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'can_pickup': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
