from django.contrib import admin
from improvetext.models import *

class ImprovementAdmin(admin.ModelAdmin):
    ordering = ("-date",)
    exclude = ("diff",)
    list_display = ("content_object", "user", "date", "applied",)
    list_filter = ("applied", "user",)
    change_form_template = "admin/improvetext/change_form.html"

admin.site.register(Improvement, ImprovementAdmin)