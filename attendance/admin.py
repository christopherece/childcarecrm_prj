from django.contrib import admin
from django.db import models
from .models import Child, Parent, Attendance, Center, Teacher, Room

@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'capacity', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('capacity',)
    ordering = ('name',)

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'center', 'created_at')
    list_filter = ('parent', 'center')
    search_fields = ('name', 'parent__name', 'center__name')
    ordering = ('-created_at',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('child', 'parent', 'center', 'sign_in', 'sign_out', 'notes')
    search_fields = ('child__name', 'parent__name', 'center__name', 'notes')
    ordering = ('-sign_in',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Add annotations for better filtering
        return queryset.annotate(
            duration=models.F('sign_out') - models.F('sign_in')
        )

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'user_full_name', 'center', 'position', 'phone', 'email', 'is_admin', 'created_at'
    )
    list_filter = ('center', 'position', 'is_admin')
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name', 
        'center__name', 'position', 'email', 'phone'
    )
    ordering = ('user__last_name', 'user__first_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Teacher Information', {
            'fields': (
                'user', 'position', 'is_admin', 'profile_picture',
                'phone', 'email', 'center', 'rooms'
            )
        }),
        ('Important dates', {
            'fields': (
                'created_at', 'updated_at'
            )
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'center')
    
    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    user_full_name.short_description = 'Full Name'

    def has_admin_access(self, obj):
        return obj.is_admin
    has_admin_access.boolean = True
    has_admin_access.short_description = 'Admin Access'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and not obj.is_admin:
            form.base_fields['is_admin'].disabled = True
        return form

    def get_today_status(self, obj):
        return obj.get_today_status()
    get_today_status.short_description = 'Status'

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'center', 'capacity', 'age_range', 'created_at')
    list_filter = ('center', 'capacity', 'age_range')
    search_fields = ('name', 'center__name', 'age_range', 'description')
    ordering = ('center', 'name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('center')
