from django.template.defaulttags import register
from nominate_app.models import datetime
from IPython import embed

@register.filter
def not_expired(end_date):
	today = datetime.today().date()
	if today < end_date:
		return True
	return False