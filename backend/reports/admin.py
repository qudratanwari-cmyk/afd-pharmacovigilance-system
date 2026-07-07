from django.contrib import admin
from .models import *

class ReportAdmin():
        # Read-only fields
    readonly_fields = (
        "registration_number",
    )


admin.site.register(Report)
admin.site.register(ReportStatus)
admin.site.register(Severity)
admin.site.register(Outcome)
admin.site.register(ReportDrug)
admin.site.register(AdverseReaction)
admin.site.register(LaboratoryInvestigation)
admin.site.register(Attachment)
admin.site.register(Review)
admin.site.register(AuditLog)
admin.site.register(Notification)
admin.site.register(StatusHistory)



