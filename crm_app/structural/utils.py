from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django_solvitize.utils.GlobalImports import TokenAuthentication as DRFTokenAuthentication
from rest_framework.authentication import get_authorization_header
from .models import StructuralReminder, StructuralNotification


def move_reminder_to_next_date(reminder):
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
        return 
    
    reminder.status = "Scheduled"
    reminder.completed_at = None
    reminder.reminder_date = next_date
    reminder.save(update_fields=["reminder_date", "status", "completed_at"])

        
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