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


# ==========================================================
# Inline Admin Classes
# ==========================================================

class ReportDrugInline(admin.TabularInline):
    """Display report drugs inside report page."""

    model = ReportDrug
    extra = 1


class AdverseReactionInline(admin.StackedInline):
    """Display adverse reactions inside report page."""

    model = AdverseReaction
    extra = 1


class AttachmentInline(admin.TabularInline):
    """Display attachments inside report page."""

    model = Attachment
    extra = 1


# ==========================================================
# Read Only Admin
# ==========================================================

class ReadOnlyAdmin(admin.ModelAdmin):
    """
    Reviewer can only view records.
    """

    def has_add_permission(self, request):

        if request.user.is_reviewer:
            return False

        return super().has_add_permission(request)


    def has_change_permission(self, request, obj=None):

        if request.user.is_reviewer:
            return False

        return super().has_change_permission(request, obj)


    def has_delete_permission(self, request, obj=None):

        if request.user.is_reviewer:
            return False

        return super().has_delete_permission(request, obj)


# ==========================================================
# Report Admin
# ==========================================================

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Admin configuration for Report model.
    """

    list_display = (
        "registration_number",
        "reporter",
        "patient",
        "status",
        "report_date",
    )

    search_fields = (
        "registration_number",
    )

    list_filter = (
        "status",
    )

    readonly_fields = (
        "registration_number",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    date_hierarchy = "report_date"

    inlines = (
        ReportDrugInline,
        AdverseReactionInline,
        AttachmentInline,
    )

    fieldsets = (

        (
            "Report Information",
            {
                "fields":(
                    "registration_number",
                    "report_date",
                    "status",
                )
            },
        ),

        (
            "Reporter Information",
            {
                "fields":(
                    "reporter",
                )
            },
        ),

        (
            "Patient Information",
            {
                "fields":(
                    "patient",
                )
            },
        ),

        (
            "Review Information",
            {
                "fields":(
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
                "fields":(
                    "reject_reason",
                    "archive_reason",
                )
            },
        ),
    )

        # ==========================================================
    # Save Report
    # ==========================================================

    def save_model(self, request, obj, form, change):
        """
        Save report, create status history,
        create audit log and assign reviewer.
        """

        previous_status = None

        # Get previous status before saving
        if change:

            previous_status = (
                Report.objects
                .only("status")
                .get(pk=obj.pk)
                .status
            )

        # Automatically assign current admin
        if not change and not obj.reviewed_by:

            obj.reviewed_by = request.user

        # Save report
        super().save_model(request, obj, form, change)

        # Save status history
        if change and previous_status != obj.status:

            StatusHistory.objects.create(

                report=obj,

                old_status=previous_status,

                new_status=obj.status,

                changed_by=request.user,
            )

        

        # Save audit log
        AuditLog.objects.create(

            user=request.user,

            action="UPDATE" if change else "CREATE",

            table_name=obj._meta.db_table,

            record_id=obj.pk,
            registration_number=obj.registration_number,

            ip_address=request.META.get("REMOTE_ADDR"),
        )


    # ==========================================================
    # Delete Report
    # ==========================================================

    def delete_model(self, request, obj):

        AuditLog.objects.create(

            user=request.user,

            action="DELETE",

            table_name=obj._meta.db_table,

            record_id=obj.pk,

            ip_address=request.META.get("REMOTE_ADDR"),
        )

        super().delete_model(request, obj)


    # ==========================================================
    # Permissions
    # ==========================================================

    def has_add_permission(self, request):

        if request.user.is_reviewer:
            return False

        return super().has_add_permission(request)


    def has_change_permission(self, request, obj=None):

        if request.user.is_reviewer:
            return False

        return super().has_change_permission(request, obj)


    def has_delete_permission(self, request, obj=None):

        if request.user.is_reviewer:
            return False

        return super().has_delete_permission(request, obj)
    

# ==========================================================
# Read Only Admin Models
# ==========================================================

@admin.register(ReportStatus)
class ReportStatusAdmin(ReadOnlyAdmin):

    list_display = (
        "status_name",
    )

    search_fields = (
        "status_name",
    )


@admin.register(Severity)
class SeverityAdmin(ReadOnlyAdmin):

    list_display = (
        "severity_name",
    )

    search_fields = (
        "severity_name",
    )


@admin.register(Outcome)
class OutcomeAdmin(ReadOnlyAdmin):

    list_display = (
        "outcome_name",
    )

    search_fields = (
        "outcome_name",
    )


@admin.register(ReportDrug)
class ReportDrugAdmin(ReadOnlyAdmin):

    list_display = (
        "report",
        "drug",
        "drug_type",
        "dose",
    )

    search_fields = (
        "report__registration_number",
        "drug__generic_name",
    )


@admin.register(AdverseReaction)
class AdverseReactionAdmin(ReadOnlyAdmin):

    list_display = (
        "report",
        "severity",
        "outcome",
    )


@admin.register(LaboratoryInvestigation)
class LaboratoryInvestigationAdmin(ReadOnlyAdmin):

    list_display = (
        "reaction",
        "investigation_type",
        "investigation_date",
    )


@admin.register(Attachment)
class AttachmentAdmin(ReadOnlyAdmin):

    list_display = (
        "report",
        "uploaded_at",
    )


@admin.register(Review)
class ReviewAdmin(ReadOnlyAdmin):

    list_display = (
        "report",
        "reviewer",
        "decision",
        "review_date",
    )


@admin.register(Notification)
class NotificationAdmin(ReadOnlyAdmin):

    list_display = (
        "report",
        "reporter",
        "notification_type",
        "delivery_status",
    )


@admin.register(StatusHistory)
class StatusHistoryAdmin(ReadOnlyAdmin):

    list_display = (
        "report",
        "old_status",
        "new_status",
        "changed_by",
        "changed_at",
    )


@admin.register(AuditLog)
class AuditLogAdmin(ReadOnlyAdmin):

    list_display = (
        "user",
        "action",
        "table_name",
        "record_id",
        "action_date",
    )

    search_fields = (
        "action",
        "table_name",
    )