from django.urls import path
from . import views

app_name = 'enrolment'

urlpatterns = [
    # Enrolment Process
    path('start/', views.enrolment_start, name='enrolment_start'),
    path('parent-guardian/<int:child_id>/', views.parent_guardian, name='parent_guardian'),
    path('medical-info/<int:child_id>/', views.medical_info, name='medical_info'),
    path('emergency-contact/<int:child_id>/', views.emergency_contact, name='emergency_contact'),
    path('enrolment-details/<int:child_id>/', views.enrolment_details, name='enrolment_details'),
    path('success/', views.enrolment_success, name='success'),

    # Admin Views
    path('list/', views.enrolment_list, name='enrolment_list'),
    path('detail/<int:enrolment_id>/', views.enrolment_detail, name='enrolment_detail'),
    path('update-status/<int:enrolment_id>/', views.update_enrolment_status, name='update_status'),
]
