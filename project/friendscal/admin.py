from django.contrib import admin

# Register your models here.
from .models import Appointment, Share

admin.site.register(Appointment)
admin.site.register(Share)