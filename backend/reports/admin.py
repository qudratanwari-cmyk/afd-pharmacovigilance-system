from django.contrib import admin

from .models import (
    Report,
    ReportStatus,
    Severity,
    Outcome,
    ReportDrug,
    AdverseReaction,
    LaboratoryInvestigation,
    Attachment,
    Review,
    AuditLog,
    Notification,
    StatusHistory,
)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for Report model.
    """

    # Display columns in report list
    list_display = (
        "registration_number",
        "reporter",
        "patient",
        "status",
        "report_date",
    )

    # Search reports by registration number
    search_fields = (
        "registration_number",
    )

    # Filter reports by status
    list_filter = (
        "status",
    )

    # Read-only fields
    readonly_fields = (
        "registration_number",
    )

    ordering = (
    "-created_at",
    )

    list_per_page = 20

    date_hierarchy = "report_date"
    


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