from django.contrib import admin

# Register your models here.

from .models import AboutUs

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id','title' , 'image')


admin.site.register(AboutUs, AboutUsAdmin)