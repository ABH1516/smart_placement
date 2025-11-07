from django.contrib import admin

# Register your models here.
from .models import DSAProblem, AptitudeQuestion
admin.site.register(DSAProblem)
admin.site.register(AptitudeQuestion)
