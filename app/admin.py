from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Aircraft)
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Booking)