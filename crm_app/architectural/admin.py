from django.contrib import admin
from .models import (
    ArchitecturalCustomer,
    ArchitecturalContact,
    ArchitecturalNote,
    ArchitecturalProject,
    ArchitecturalReminder,
    ArchitecturalCalendarActivity,
    ArchitecturalNotification,
)


# ----------------------------
# Architectural Customer Admin
# ----------------------------
@admin.register(ArchitecturalCustomer)
class ArchitecturalCustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'company_name',
        'category',
        'lead_status',
        'project_status',
        'added_by',
        'created_at',
    )
    search_fields = ('company_name', 'phone', 'email')
    list_filter = ('category', 'lead_status', 'project_status')
    ordering = ('-created_at',)


# ----------------------------
# Architectural Contact Admin
# ----------------------------
@admin.register(ArchitecturalContact)
class ArchitecturalContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role', 'company', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-id',)


# ----------------------------
# Architectural Note Admin
# ----------------------------
@admin.register(ArchitecturalNote)
class ArchitecturalNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'created_by', 'created_at')
    search_fields = ('note',)
    ordering = ('-created_at',)


# ----------------------------
# Architectural Project Admin
# ----------------------------
@admin.register(ArchitecturalProject)
class ArchitecturalProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'status')
    search_fields = ('name', 'company__company_name')
    list_filter = ('status',)
    ordering = ('-id',)


# ----------------------------
# Architectural Reminder Admin
# ----------------------------
@admin.register(ArchitecturalReminder)
class ArchitecturalReminderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'company',
        'project',
        'assigned_to',
        'frequency',
        'reminder_date',
        'status',
        'completed_at',
    )

    list_filter = (
        'status',
        'frequency',
        'assigned_to',
    )

    search_fields = (
        'company__company_name',
        'assigned_to__username',
    )

    ordering = ('-reminder_date',)

    readonly_fields = (
        'completed_at',
        'created_at',
    )


# ----------------------------
# Architectural Calendar Activity Admin
# ----------------------------
@admin.register(ArchitecturalCalendarActivity)
class ArchitecturalCalendarActivityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'activity',
        'company',
        'user',
        'related_reminder',
        'created_at',
    )
    search_fields = ('description',)
    ordering = ('-activity',)


# ----------------------------
# Architectural Notification Admin
# ----------------------------
@admin.register(ArchitecturalNotification)
class ArchitecturalNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sales_person',
        'company',
        'reminder',
        'read',
        'created_at',
    )
    list_filter = ('read',)
    search_fields = ('company__company_name',)
    ordering = ('-created_at',)
