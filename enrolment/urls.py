from django.urls import path
from . import views

app_name = 'enrolment'

urlpatterns = [
    # Enrolment Process
    path('start/', views.enrolment_start, name='enrolment_start'),
    path('parent-guardian/', views.parent_guardian, name='parent_guardian'),
    path('medical-info/', views.medical_info, name='medical_info'),
    path('emergency-contact/', views.emergency_contact, name='emergency_contact'),
    path('enrolment-details/', views.enrolment_details, name='enrolment_details'),
    path('success/', views.success, name='success'),
    path('api/rooms/<int:center_id>/', views.get_rooms, name='api_rooms'),

    # Admin Views
    path('list/', views.enrolment_list, name='enrolment_list'),
    path('detail/<int:enrolment_id>/', views.enrolment_detail, name='enrolment_detail'),
    path('update-status/<int:enrolment_id>/', views.update_enrolment_status, name='update_status'),
]
