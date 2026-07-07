from django.contrib import admin

from .models import Province, Gender, Language, Setting


admin.site.register(Province)
admin.site.register(Gender)
admin.site.register(Language)
admin.site.register(Setting)