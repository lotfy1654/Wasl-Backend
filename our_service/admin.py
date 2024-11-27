from django.contrib import admin

# Register your models here.

from .models import Service, ServiceStep, ServiceOrder, ServiceOrderStep

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'total_price']

class ServiceStepAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'service', 'status', 'step_price' , 'payment_status']

class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'service', 'status', 'assigned_employee', 'created_at']

class ServiceOrderStepAdmin(admin.ModelAdmin):
        list_display = ['id','order', 'step', 'status', 'payment_status']
        
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceStep , ServiceStepAdmin)
admin.site.register(ServiceOrder , ServiceOrderAdmin)
admin.site.register(ServiceOrderStep , ServiceOrderStepAdmin)