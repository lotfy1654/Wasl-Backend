from django.contrib import admin

# Register your models here.

from .models import AllUsers

class AllUsersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'id','username', 'role', 'date_joined' , 'is_staff' , 'is_active' , 'is_superuser')

admin.site.register(AllUsers, AllUsersAdmin)