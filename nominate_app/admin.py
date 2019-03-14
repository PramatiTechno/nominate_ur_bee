from django.contrib import admin

# Register your models here.
from .models import*

admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(Awards)
admin.site.register(NominationPeriod)
admin.site.register(NominationPeriodFrequency)
admin.site.register(AwardTemplate)
admin.site.register(Questions)
admin.site.register(NominationTimeSlot)
admin.site.register(NominationInstance)