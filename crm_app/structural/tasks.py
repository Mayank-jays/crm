from celery import shared_task
from django.utils import timezone
from django.db import transaction

from .models import StructuralReminder, StructuralNotification, StructuralCalendarActivity


@shared_task
def process_due_reminders():
    """
    Marks due reminders as Pending and sends notifications
    """
    today = timezone.now().date()

    reminders = StructuralReminder.objects.filter(
        reminder_date__lte=today,
        status='Scheduled'
    )

    for reminder in reminders:
        with transaction.atomic():
            reminder.status = 'Pending'
            reminder.save(update_fields=['status'])

            # Notification
            StructuralNotification.objects.create(
                sales_person=reminder.assigned_to,
                company=reminder.company,
                title="Reminder Due",
                message=f"Reminder for {reminder.company.company_name}",
                reminder=reminder
            )

            
