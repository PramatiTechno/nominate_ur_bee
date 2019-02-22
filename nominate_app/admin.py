from django.contrib import admin

# Register your models here.
from .models import*

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Awards)
admin.site.register(NominationPeriod)
admin.site.register(AwardTemplate)
admin.site.register(Questions)