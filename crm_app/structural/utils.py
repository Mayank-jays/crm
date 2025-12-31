from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django_solvitize.utils.GlobalImports import TokenAuthentication as DRFTokenAuthentication
from rest_framework.authentication import get_authorization_header

from .models import StructuralReminder
from .models import StructuralReminder, StructuralNotification


def create_next_recurring_reminder(reminder):
    """
    Auto-create next recurring reminder after completion
    """

    if reminder.frequency == "Weekly":
        next_date = reminder.reminder_date + timedelta(days=7)

    elif reminder.frequency == "Monthly":
        next_date = reminder.reminder_date + relativedelta(months=1)

    elif reminder.frequency == "Yearly":
        next_date = reminder.reminder_date + relativedelta(years=1)

    else:
        # Custom / None → no recurrence
        return None

    return StructuralReminder.objects.create(
        company=reminder.company,
        project=getattr(reminder, "project", None),
        assigned_to=reminder.assigned_to,
        reminder_date=next_date,
        frequency=reminder.frequency,
        status="Scheduled"   # 🔑 IMPORTANT
    )

def process_today_reminders():
    """
    Move today's scheduled reminders to pending
    and create notifications
    """
    today = timezone.now().date()

    reminders = StructuralReminder.objects.filter(
        reminder_date=today,
        status='Scheduled'
    )

    for r in reminders:
        r.status = 'Pending'
        r.save(update_fields=["status"])

        # Avoid duplicate notifications
        if not StructuralNotification.objects.filter(reminder=r).exists():
            StructuralNotification.objects.create(
                sales_person=r.assigned_to,
                company=r.company,
                reminder=r,
                title="Reminder Due Today",
                message=f"Follow-up for {r.company.company_name}"
            )
        
class BearerOrTokenAuthentication(DRFTokenAuthentication):
    def authenticate(self, request):
        raw = get_authorization_header(request)
        if not raw:
            return super().authenticate(request)
        header = raw.decode('utf-8').strip()
        lower = header.lower()
        token_value = None
        if lower.startswith('bearer '):
            token_value = header.split(' ', 1)[1].strip()
        elif lower.startswith('token '):
            token_value = header.split(' ', 1)[1].strip()
        if token_value:
            if token_value.lower().startswith('token '):
                token_value = token_value.split(' ', 1)[1].strip()
            request.META['HTTP_AUTHORIZATION'] = f'Token {token_value}'
        return super().authenticate(request)