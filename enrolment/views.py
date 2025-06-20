from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from attendance.decorators import admin_required
from .models import Enrolment, ParentGuardian, MedicalInformation, EmergencyContact
from .forms import EnrolmentForm, ParentGuardianForm, MedicalInformationForm, EmergencyContactForm, ChildForm
from attendance.models import Child, Parent, Center, Room

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
            # Create a temporary parent for the child
            parent = Parent.objects.create(
                name=f"Parent for {child_form.cleaned_data['name']}",
                email=f"{child_form.cleaned_data['name'].lower().replace(' ', '')}@temp.com"
            )
            child = child_form.save(commit=False)
            child.parent = parent
            child.save()
            return redirect('enrolment:parent_guardian', child_id=child.id)
    else:
        child_form = ChildForm()
    return render(request, 'enrolment/enrolment_start.html', {'child_form': child_form})

def parent_guardian(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    parent = child.parent
    
    if request.method == 'POST':
        parent_form = ParentGuardianForm(request.POST)
        if parent_form.is_valid():
            parent_guardian = parent_form.save(commit=False)
            parent_guardian.parent = parent
            parent_guardian.child = child
            
            # Handle empty values by checking if the field exists
            first_name = parent_form.cleaned_data.get('first_name', '')
            last_name = parent_form.cleaned_data.get('last_name', '')
            email = parent_form.cleaned_data.get('email', '')
            phone_number = parent_form.cleaned_data.get('phone_number', '')
            
            # Only update fields if they have values
            if first_name:
                parent_guardian.first_name = first_name
            if last_name:
                parent_guardian.last_name = last_name
            if email:
                parent_guardian.email = email
            if phone_number:
                parent_guardian.phone_number = phone_number
            
            parent_guardian.save()
            
            # Update the parent's name only if we have both first and last name
            if first_name and last_name:
                parent.name = f"{first_name} {last_name}"
            if email:
                parent.email = email
            
            parent.save()
            return redirect('enrolment:medical_info', child_id=child_id)
    else:
        parent_form = ParentGuardianForm(instance=parent)
    return render(request, 'enrolment/parent_guardian.html', {
        'child': child,
        'parent_form': parent_form
    })

def medical_info(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    
    if request.method == 'POST':
        medical_form = MedicalInformationForm(request.POST, request.FILES)
        if medical_form.is_valid():
            medical_info = medical_form.save(commit=False)
            medical_info.child = child
            medical_info.save()
            return redirect('enrolment:emergency_contact', child_id=child_id)
    else:
        medical_form = MedicalInformationForm()
    return render(request, 'enrolment/medical_info.html', {
        'child': child,
        'medical_form': medical_form
    })

def emergency_contact(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    # Get the first emergency contact for this child if it exists
    try:
        emergency_contact = EmergencyContact.objects.filter(child=child).first()
    except EmergencyContact.DoesNotExist:
        emergency_contact = None
    
    if request.method == 'POST':
        emergency_form = EmergencyContactForm(request.POST, instance=emergency_contact)
        if emergency_form.is_valid():
            emergency = emergency_form.save(commit=False)
            emergency.child = child
            emergency.save()
            return redirect('enrolment:enrolment_details', child_id=child_id)
    else:
        emergency_form = EmergencyContactForm(instance=emergency_contact)
    return render(request, 'enrolment/emergency_contact.html', {
        'child': child,
        'form': emergency_form
    })

def enrolment_details(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    centers = Center.objects.all()
    
    if request.method == 'POST':
        enrolment_form = EnrolmentForm(request.POST)
        if enrolment_form.is_valid():
            enrolment = enrolment_form.save(commit=False)
            enrolment.child = child
            enrolment.save()
            
            # Update the child's center and room
            child.center = enrolment.center
            child.room = enrolment.room
            child.save()
            
            messages.success(request, 'Enrolment application submitted successfully!')
            return redirect('enrolment:success')
    else:
        enrolment_form = EnrolmentForm()
    
    return render(request, 'enrolment/enrolment_details.html', {
        'child': child,
        'enrolment_form': enrolment_form,
        'centers': centers
    })

def enrolment_success(request):
    return render(request, 'enrolment/enrolment_success.html')

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
