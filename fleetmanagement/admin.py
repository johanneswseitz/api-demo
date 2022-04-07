from django.contrib import admin
from .models import Auto


# Register your models here.
class AutoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Auto, AutoAdmin)
