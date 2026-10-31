from django.contrib import admin
from .models import HuntLog, WantedCriminal

admin.site.register(WantedCriminal)
admin.site.register(HuntLog)
