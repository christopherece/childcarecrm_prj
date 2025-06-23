from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import Enrolment, Child, ParentGuardian, MedicalInformation, EmergencyContact
from .forms import EnrolmentForm, ChildForm, ParentGuardianForm, MedicalInformationForm, EmergencyContactForm
from attendance.decorators import admin_required
from attendance.models import Center, Room, Parent
import json
from datetime import datetime, date

@admin_required
def get_rooms(request, center_id):
    try:
        center = Center.objects.get(id=center_id)
        rooms = Room.objects.filter(center=center).order_by('name')
        return JsonResponse([{'id': room.id, 'name': room.name} for room in rooms], safe=False)
    except Center.DoesNotExist:
        return JsonResponse([], safe=False)

@admin_required
def enrolment_start(request):
    if request.method == 'POST':
        child_form = ChildForm(request.POST, request.FILES)
        if child_form.is_valid():
            # Get cleaned data
            cleaned_data = child_form.cleaned_data
            
            # Create child data dictionary with proper date handling
            child_data = {
                'name': cleaned_data['name'],
                'date_of_birth': cleaned_data['date_of_birth'].isoformat(),
                'gender': cleaned_data['gender'],
                'emergency_contact': cleaned_data['emergency_contact'],
                'emergency_phone': cleaned_data['emergency_phone'],
                'center_id': cleaned_data['center'].id if cleaned_data['center'] else None
            }
            
            # Store in session
            enrolment_data = {
                'child': child_data,
                'step': 'start'
            }
            
            # Convert to JSON string
            request.session['enrolment_data'] = json.dumps(enrolment_data)
            
            return redirect('enrolment:parent_guardian')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        child_form = ChildForm()
    return render(request, 'enrolment/enrolment_start.html', {'child_form': child_form})

@admin_required
def parent_guardian(request):
    # Get session data
    enrolment_data_json = request.session.get('enrolment_data', '{}')
    try:
        enrolment_data = json.loads(enrolment_data_json)
    except json.JSONDecodeError:
        messages.error(request, "Invalid session data. Please start the enrolment process again.")
        return redirect('enrolment:enrolment_start')
    
    # Validate child data
    child_data = enrolment_data.get('child', {})
    if not all([child_data.get('name'), child_data.get('date_of_birth'), child_data.get('gender')]):
        messages.error(request, "Child information is incomplete. Please go back and complete the child information step.")
        return redirect('enrolment:enrolment_start')
    
    if request.method == 'POST':
        parent_form = ParentGuardianForm(request.POST)
        if parent_form.is_valid():
            # Update enrolment data
            enrolment_data['parent_guardian'] = parent_form.cleaned_data
            enrolment_data['step'] = 'parent_guardian'
            
            # Store updated data
            request.session['enrolment_data'] = json.dumps(enrolment_data)
            return redirect('enrolment:medical_info')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        parent_form = ParentGuardianForm()
    
    return render(request, 'enrolment/parent_guardian.html', {
        'parent_form': parent_form,
        'child_data': child_data
    })

@admin_required
def medical_info(request):
    enrolment_data_json = request.session.get('enrolment_data', '{}')
    try:
        enrolment_data = json.loads(enrolment_data_json)
    except json.JSONDecodeError:
        messages.error(request, "Invalid session data. Please start the enrolment process again.")
        return redirect('enrolment:enrolment_start')
    
    if request.method == 'POST':
        medical_form = MedicalInformationForm(request.POST, request.FILES)
        if medical_form.is_valid():
            # Get cleaned data including file
            medical_data = medical_form.cleaned_data
            
            # Convert file data to string for JSON serialization
            if 'immunization_record' in medical_data:
                medical_data['immunization_record'] = str(medical_data['immunization_record'])
            
            enrolment_data['medical_info'] = medical_data
            enrolment_data['step'] = 'medical_info'
            request.session['enrolment_data'] = json.dumps(enrolment_data)
            return redirect('enrolment:emergency_contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        medical_form = MedicalInformationForm()
    
    return render(request, 'enrolment/medical_info.html', {
        'medical_form': medical_form,
        'child_data': enrolment_data.get('child', {})
    })

@admin_required
def emergency_contact(request):
    enrolment_data_json = request.session.get('enrolment_data', '{}')
    try:
        enrolment_data = json.loads(enrolment_data_json)
    except json.JSONDecodeError:
        messages.error(request, "Invalid session data. Please start the enrolment process again.")
        return redirect('enrolment:enrolment_start')
    
    if request.method == 'POST':
        contact_form = EmergencyContactForm(request.POST)
        if contact_form.is_valid():
            enrolment_data['emergency_contact'] = contact_form.cleaned_data
            enrolment_data['step'] = 'emergency_contact'
            request.session['enrolment_data'] = json.dumps(enrolment_data)
            return redirect('enrolment:enrolment_details')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        contact_form = EmergencyContactForm()
    
    return render(request, 'enrolment/emergency_contact.html', {
        'contact_form': contact_form,
        'child_data': enrolment_data.get('child', {})
    })

@admin_required
def enrolment_details(request):
    enrolment_data_json = request.session.get('enrolment_data', '{}')
    try:
        enrolment_data = json.loads(enrolment_data_json)
    except json.JSONDecodeError:
        messages.error(request, "Invalid session data. Please start the enrolment process again.")
        return redirect('enrolment:enrolment_start')
    
    if request.method == 'POST':
        enrolment_form = EnrolmentForm(request.POST)
        if enrolment_form.is_valid():
            try:
                # Get session data
                enrolment_data_json = request.session.get('enrolment_data', '{}')
                enrolment_data = json.loads(enrolment_data_json)
                
                # Validate required data
                if not all([
                    enrolment_data.get('child', {}).get('name'),
                    enrolment_data.get('child', {}).get('date_of_birth'),
                    enrolment_data.get('child', {}).get('gender'),
                    enrolment_data.get('parent_guardian', {}).get('email')
                ]):
                    messages.error(request, "Missing required information")
                    return redirect('enrolment:enrolment_start')
                
                # Get center and room from form data
                center_id = enrolment_form.cleaned_data['center'].id
                room_id = enrolment_form.cleaned_data['room'].id
                
                # Create parent
                parent_data = enrolment_data.get('parent_guardian', {})
                parent, created = Parent.objects.get_or_create(
                    email=parent_data.get('email'),
                    defaults={
                        'name': f"{parent_data.get('first_name')} {parent_data.get('last_name')}",
                        'phone': parent_data.get('phone_number'),
                        'address': parent_data.get('address')
                    }
                )
                
                # Create child
                child_data = enrolment_data.get('child', {})
                child = Child.objects.create(
                    name=child_data.get('name'),
                    date_of_birth=datetime.fromisoformat(child_data.get('date_of_birth')).date(),
                    gender=child_data.get('gender'),
                    emergency_contact=child_data.get('emergency_contact'),
                    emergency_phone=child_data.get('emergency_phone'),
                    parent=parent,
                    center=Center.objects.get(id=center_id),
                    room=Room.objects.get(id=room_id)
                )
                
                # Create medical info
                medical_data = enrolment_data.get('medical_info', {})
                try:
                    medical_info = MedicalInformation.objects.create(
                        child=child,
                        allergies=medical_data.get('allergies', ''),
                        medical_conditions=medical_data.get('medical_conditions', ''),
                        medications=medical_data.get('medications', ''),
                        medical_notes=medical_data.get('medical_notes', '')
                    )
                    
                    # Save immunization record if provided
                    immunization_record = medical_data.get('immunization_record')
                    if immunization_record:
                        medical_info.immunization_record = immunization_record
                        medical_info.save()
                    
                except Exception as e:
                    messages.error(request, f"Error saving medical information: {str(e)}")
                    return redirect('enrolment:medical_info')
                
                # Create emergency contact
                contact_data = enrolment_data.get('emergency_contact', {})
                EmergencyContact.objects.create(
                    child=child,
                    first_name=contact_data.get('first_name'),
                    last_name=contact_data.get('last_name'),
                    relationship=contact_data.get('relationship'),
                    phone_number=contact_data.get('phone_number'),
                    email=contact_data.get('email'),
                    address=contact_data.get('address'),
                    can_pickup=contact_data.get('can_pickup', False)
                )
                
                # Get center and room from form data
                center = enrolment_form.cleaned_data.get('center')
                room = enrolment_form.cleaned_data.get('room')
                
                # Create enrolment with center and room
                enrolment = enrolment_form.save(commit=False)
                enrolment.child = child
                enrolment.save()
                
                # Update child with center information
                child.center = center
                child.room = room
                child.save()
                
                # Clear session data
                del request.session['enrolment_data']
                
                return redirect('enrolment:success')

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('enrolment:enrolment_start')

        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'enrolment/enrolment_details.html', {
                'enrolment_form': enrolment_form,
                'child_data': enrolment_data.get('child', {})
            })
    else:
        enrolment_form = EnrolmentForm()
        return render(request, 'enrolment/enrolment_details.html', {
            'enrolment_form': enrolment_form,
            'child_data': enrolment_data.get('child', {})
        })
    # Get all centers for the dropdown
    centers = Center.objects.all()
    
    # Get child data from session
    child_data = enrolment_data.get('child', {})
    
    # Convert date string back to date object if present
    if isinstance(child_data, dict) and 'date_of_birth' in child_data:
        try:
            dob_str = child_data['date_of_birth']
            if dob_str:  # Check if string is not empty
                child_data['date_of_birth'] = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            pass

    # Format date for display
    dob_display = child_data.get('date_of_birth', '')
    if isinstance(dob_display, date):
        dob_display = dob_display.strftime('%Y-%m-%d')
    else:
        dob_display = ''

    return render(request, 'enrolment/enrolment_details.html', {
        'enrolment_form': enrolment_form,
        'child_data': child_data,
        'centers': centers,
        'child_name': child_data.get('name', ''),
        'child_dob': dob_display if dob_display else '',
        'child_gender': child_data.get('gender', '')
    })

@admin_required
def success(request):
    return render(request, 'enrolment/enrolment_success.html')

@admin_required
def enrolment_list(request):
    enrolments = Enrolment.objects.all().order_by('-enrolment_date')
    return render(request, 'enrolment/enrolment_list.html', {'enrolments': enrolments})

def enrolment_detail(request, enrolment_id):
    enrolment = get_object_or_404(Enrolment, id=enrolment_id)
    return render(request, 'enrolment/enrolment_detail.html', {'enrolment': enrolment})

def update_enrolment_status(request, enrolment_id):
    enrolment = get_object_or_404(Enrolment, id=enrolment_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Enrolment.STATUS_CHOICES):
            enrolment.status = status
            enrolment.save()
            messages.success(request, f'Enrolment status updated to {enrolment.get_status_display()}')
            return redirect('enrolment:enrolment_detail', enrolment_id=enrolment_id)
    return redirect('enrolment:enrolment_list')
