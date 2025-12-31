from django.urls import path
from .views import (
    ArchitecturalCustomerAPI,
    SalesRepDropdownAPI,
    SharedCalendarAPIView,
    MyNotificationsAPIView,
    AcknowledgeReminderAPIView,
    MyRemindersAPIView,
    ArchitecturalCategoriesAPIView
)

urlpatterns = [
    path('architectural/clients/', ArchitecturalCustomerAPI.as_view(), name='Architectural-company-list'),  # GET list / POST create
    path('architectural/clients/<int:id>/', ArchitecturalCustomerAPI.as_view(), name='Architectural-company-detail'),  # GET, PUT, DELETE
    path('architectural/clients/category/', ArchitecturalCategoriesAPIView.as_view(), name='Architectural-company-category'),
    path('architectural/sales-rep-dropdown/', SalesRepDropdownAPI.as_view(), name='Architectural-sales-rep-dropdown'),
    path('architectural/calendar/', SharedCalendarAPIView.as_view(), name='Architectural-shared-calendar'),
    path('architectural/notifications/', MyNotificationsAPIView.as_view(), name='Architectural-my-notifications'),
    path('architectural/reminders/<int:reminder_id>/acknowledge/', AcknowledgeReminderAPIView.as_view(), name='acknowledge-reminder'),
    path('architectural/my-reminders/', MyRemindersAPIView.as_view(), name='my-reminders'),
    path('architectural/clients/category/', ArchitecturalCategoriesAPIView.as_view(), name='Architectural-company-category'),
    
]
