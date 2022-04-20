from django.contrib import admin
from .models import Appointment, Tenant, Payment_Tenant, Report_Tenant, Tenant_Favourite
# Register your models here.
admin.site.register(Tenant)
admin.site.register(Appointment)
admin.site.register(Payment_Tenant)
admin.site.register(Report_Tenant)
admin.site.register(Tenant_Favourite)
