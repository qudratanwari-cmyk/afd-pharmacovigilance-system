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

# Inline Admin for Report Drugs
# ==========================================
class ReportDrugInline(admin.TabularInline):
    """
    Display report drugs inside Report admin page.
    """

    model = ReportDrug

    extra = 1


# ==========================================
# Inline Admin for Adverse Reactions
# ==========================================
class AdverseReactionInline(admin.StackedInline):
    """
    Display adverse reactions inside Report admin page.
    """

    model = AdverseReaction

    extra = 1


# ==========================================
# Inline Admin for Attachments
# ==========================================
class AttachmentInline(admin.TabularInline):
    """
    Display attachments inside Report admin page.
    """

    model = Attachment

    extra = 1





class ReadOnlyAdmin(admin.ModelAdmin):
    """
    Read-only admin for Reviewer users.
    """

    def has_add_permission(self, request):

        if request.user.role and request.user.role.role_name:
            return False

        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):

        if request.user.role and request.user.role.role_name:
            return False

        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):

        if request.user.role and request.user.role.role_name:
            return False

        return super().has_delete_permission(request, obj)

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

    # Organize report fields into logical sections
    fieldsets = (

        (
            "Report Information",
            {
                "fields": (
                    "registration_number",
                    "report_date",
                    "status",
                )
            },
        ),

        (
            "Reporter Information",
            {
                "fields": (
                    "reporter",
                )
            },
        ),

        (
            "Patient Information",
            {
                "fields": (
                    "patient",
                )
            },
        ),

        (
            "Review Information",
            {
                "fields": (
                    "reviewed_by",
                    "approved_by",
                    "approved_date",
                    "closed_date",
                )
            },
        ),

        (
            "Remarks",
            {
                "fields": (
                    "reject_reason",
                    "archive_reason",
                )
            },
        ),
    )

        # Display related models inside Report page
    inlines = (
        ReportDrugInline,
        AdverseReactionInline,
        AttachmentInline,
    )

    # Automatically save status history when status changes
    def save_model(self, request, obj, form, change):

        if change:

            previous = Report.objects.get(pk=obj.pk)

            if previous.status != obj.status:

                StatusHistory.objects.create(

                    report=obj,

                    old_status=previous.status,

                    new_status=obj.status,

                    changed_by=request.user,

                )

        super().save_model(request, obj, form, change)


        # Save audit log after creating or updating a report
    def save_model(self, request, obj, form, change):

        # Save status history
        if change:

            previous = Report.objects.get(pk=obj.pk)

            if previous.status != obj.status:

                StatusHistory.objects.create(

                    report=obj,
                    old_status=previous.status,
                    new_status=obj.status,
                    changed_by=request.user,
                )

        super().save_model(request, obj, form, change)

        # Save audit log
        AuditLog.objects.create(

            user=request.user,

            action="Updated Report" if change else "Created Report",

            table_name="reports",

            record_id=obj.id,

            ip_address=request.META.get("REMOTE_ADDR"),
        )  
    # Save audit log when deleting a report
    def delete_model(self, request, obj):

        AuditLog.objects.create(

            user=request.user,

            action="Deleted Report",

            table_name="reports",

            record_id=obj.id,

            ip_address=request.META.get("REMOTE_ADDR"),
        )

        super().delete_model(request, obj) 

    # Automatically assign current admin as reviewer
    def save_model(self, request, obj, form, change):

        # Assign reviewer only for new reports
        if not change and not obj.reviewed_by:
            obj.reviewed_by = request.user

        super().save_model(request, obj, form, change)
    
    # Reviewer can only view reports
    def has_change_permission(self, request, obj=None):

        if request.user.role and request.user.role.role_name:
            return False

        return super().has_change_permission(request, obj)

    # Reviewer cannot delete reports
    def has_delete_permission(self, request, obj=None):

        if request.user.role and request.user.role.role_name:
            return False

        return super().has_delete_permission(request, obj)
    
    # Reviewer cannot create reports
    def has_add_permission(self, request):

        if request.user.role and request.user.role.role_name:
            return False

        return super().has_add_permission(request)


 
    #Reviewer can only view records.
    
@admin.register(ReportStatus)
class ReportStatusAdmin(ReadOnlyAdmin):
    pass


@admin.register(Severity)
class SeverityAdmin(ReadOnlyAdmin):
    pass


@admin.register(Outcome)
class OutcomeAdmin(ReadOnlyAdmin):
    pass


@admin.register(ReportDrug)
class ReportDrugAdmin(ReadOnlyAdmin):
    pass


@admin.register(AdverseReaction)
class AdverseReactionAdmin(ReadOnlyAdmin):
    pass


@admin.register(LaboratoryInvestigation)
class LaboratoryInvestigationAdmin(ReadOnlyAdmin):
    pass


@admin.register(Attachment)
class AttachmentAdmin(ReadOnlyAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(ReadOnlyAdmin):
    pass


@admin.register(AuditLog)
class AuditLogAdmin(ReadOnlyAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(ReadOnlyAdmin):
    pass


@admin.register(StatusHistory)
class StatusHistoryAdmin(ReadOnlyAdmin):
    pass