from django.contrib import admin

from .models import Team
from .models import Contest

admin.site.register(Team)
admin.site.register(Contest)