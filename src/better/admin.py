from django.contrib import admin

from .models import Team
from .models import Contest
from better.models import AvailableBets

admin.site.register(Team)
admin.site.register(Contest)
admin.site.register(AvailableBets)