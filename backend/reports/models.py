
from accounts.models import User
from reporters.models import Reporter
from patients.models import Patient
from drugs.models import Drug, DrugType
from django.db import models

from django.core.exceptions import ValidationError

# Generate current year
from datetime import datetime

# Database transaction support
from django.db import transaction

from django.utils import timezone

class ReportStatus(models.Model):

    status_name=models.CharField(max_length=50,unique=True)

    class Meta:
        db_table="report_statuses"

    def __str__(self):
        return self.status_name


class Severity(models.Model):

    severity_name=models.CharField(max_length=100,unique=True)

    class Meta:
        db_table="severities"

    def __str__(self):
        return self.severity_name


class Outcome(models.Model):

    outcome_name=models.CharField(max_length=100,unique=True)

    class Meta:
        db_table="outcomes"

    def __str__(self):
        return self.outcome_name



class Report(models.Model):
    
    # Unique report registration number
    registration_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        editable=False
    )

    reporter=models.ForeignKey(Reporter,on_delete=models.PROTECT)

    patient=models.ForeignKey(Patient,on_delete=models.PROTECT)

    status = models.ForeignKey(
    ReportStatus,
    on_delete=models.PROTECT,
    default=1)

    reviewed_by=models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_reports"
    )

    approved_by=models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_reports"
    )

    # Automatically use today's date for new reports
    report_date = models.DateField(
        default=timezone.now
    )

    approved_date=models.DateField(null=True,blank=True)

    closed_date=models.DateField(null=True,blank=True)

    reject_reason=models.TextField(blank=True)

    archive_reason=models.TextField(blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    
    # Automatically generate registration number and assign Pending status
    def save(self, *args, **kwargs):

        # Generate registration number only once
        if not self.registration_number:

            current_year = datetime.now().year

            with transaction.atomic():

                last_report = (
                    Report.objects
                    .select_for_update()
                    .order_by("-id")
                    .first()
                )

                if last_report and last_report.registration_number:

                    last_number = int(
                        last_report.registration_number.split("-")[-1]
                    ) + 1

                else:

                    last_number = 1

                self.registration_number = (
                    f"PV-{current_year}-{last_number:06d}"
                )
        # Run model validation before saving
        self.full_clean()

        super().save(*args, **kwargs)

    # Validate report business rules
    def clean(self):

        # Get current status name
        status_name = self.status.status_name.lower()

                # ==========================================================
        # Validate patient information for Health Facility reports
        # ==========================================================

        reporter_code = self.reporter.reporter_type.code

        if self.reporter.reporter_type.code == "HF":

            if not self.patient.gender_id:
                raise ValidationError({
                    "patient": "Patient gender is required."
                })

            if self.patient.weight is None:
                raise ValidationError({
                    "patient": "Patient weight is required."
                })

            if self.patient.height is None:
                raise ValidationError({
                    "patient": "Patient height is required."
                })

            # Pregnancy and breastfeeding are required only for female patients
            if self.patient.gender.gender_name.lower() == "female":

                if self.patient.is_pregnant is None:
                    raise ValidationError({
                        "patient": "Pregnancy status is required."
                    })

                if self.patient.is_breast_feeding is None:
                    raise ValidationError({
                        "patient": "Breastfeeding status is required."
                    })

        # Approved reports must have approver and approval date
        if status_name == "approved":

            if not self.approved_by:
                raise ValidationError({
                    "approved_by": "Approved By is required."
                })

            if not self.approved_date:
                raise ValidationError({
                    "approved_date": "Approved Date is required."
                })
        
        if status_name == "rejected":

            if not self.reject_reason:
                raise ValidationError({
                    "reject_reason": "Reject reason is required."
                })
        
        if status_name == "archived":

            if not self.archive_reason:
                raise ValidationError({
                    "archive_reason": "Archive reason is required."
                })
        # Approved date cannot be earlier than report date
        if self.approved_date and self.report_date:

            if self.approved_date < self.report_date:

                raise ValidationError({
                    "approved_date": "Approved Date cannot be earlier than Report Date."
                })
    class Meta:
        db_table="reports"

    def __str__(self):
        return self.registration_number


class ReportDrug(models.Model):

    report=models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name="report_drugs"
    )

    drug=models.ForeignKey(
        Drug,
        on_delete=models.PROTECT
    )

    drug_type=models.ForeignKey(
        DrugType,
        on_delete=models.PROTECT
    )

    dose=models.CharField(max_length=100)

    route=models.CharField(max_length=100)

    frequency=models.CharField(max_length=100)

    indication=models.TextField(blank=True)

    treatment_start_date=models.DateField(null=True,blank=True)

    treatment_stop_date=models.DateField(null=True,blank=True)

    treatment_duration=models.CharField(max_length=100,blank=True)

    is_treatment_ongoing=models.BooleanField(default=False)

    # Validate treatment dates
    def clean(self):

        # Stop date cannot be earlier than start date
        if self.treatment_start_date and self.treatment_stop_date:

            if self.treatment_stop_date < self.treatment_start_date:

                raise ValidationError({
                    "treatment_stop_date":
                    "Treatment Stop Date cannot be earlier than Treatment Start Date."
                })

    # Validate before saving
    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    class Meta:
        db_table="report_drugs"
class AdverseReaction(models.Model):

    report=models.ForeignKey(Report,on_delete=models.CASCADE)

    reaction_start_date=models.DateField(null=True,blank=True)

    reaction_end_date=models.DateField(null=True,blank=True)

    reaction_description=models.TextField()

    medical_history=models.TextField(blank=True)

    allergy_history=models.TextField(blank=True)

    time_interval_drug_reaction=models.CharField(max_length=100,blank=True)

    drug_stopped=models.BooleanField(default=False)

    reaction_reduce_after_stopping=models.BooleanField(default=False)

    dose_reduced=models.BooleanField(default=False)

    reaction_reduce_after_dose_reduction=models.BooleanField(default=False)

    drug_restarted=models.BooleanField(default=False)

    reaction_returned_after_restart=models.BooleanField(default=False)

    severity=models.ForeignKey(Severity,on_delete=models.SET_NULL,null=True)

    outcome=models.ForeignKey(Outcome,on_delete=models.SET_NULL,null=True)

    # Validate adverse reaction dates
    def clean(self):

        # End date cannot be earlier than start date
        if self.reaction_start_date and self.reaction_end_date:

            if self.reaction_end_date < self.reaction_start_date:

                raise ValidationError({
                    "reaction_end_date":
                    "Reaction End Date cannot be earlier than Reaction Start Date."
                })
    # Validate before saving
    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    class Meta:
        db_table="adverse_reactions"

class LaboratoryInvestigation(models.Model):

    reaction=models.ForeignKey(
        AdverseReaction,
        on_delete=models.CASCADE
    )

    investigation_type=models.CharField(max_length=200)

    investigation_result=models.TextField(blank=True)

    investigation_date=models.DateField(null=True,blank=True)

    class Meta:
        db_table="laboratory_investigations"

class Attachment(models.Model):

    report=models.ForeignKey(Report,on_delete=models.CASCADE)

    file=models.FileField(upload_to="attachments/")

    description=models.TextField(blank=True)

    uploaded_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table="attachments"
class Review(models.Model):

    report=models.ForeignKey(Report,on_delete=models.CASCADE)

    reviewer=models.ForeignKey(User,on_delete=models.PROTECT)

    decision=models.CharField(max_length=30)

    review_comment=models.TextField(blank=True)

    review_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table="reviews"


class AuditLog(models.Model):

    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    action=models.CharField(max_length=100)

    table_name=models.CharField(max_length=100)

    record_id=models.IntegerField()

    action_date=models.DateTimeField(auto_now_add=True)

    registration_number = models.CharField(max_length=50, null=True)

    ip_address=models.GenericIPAddressField()

    class Meta:
        db_table="audit_logs"

class Notification(models.Model):

    report=models.ForeignKey(Report,on_delete=models.CASCADE)

    reporter=models.ForeignKey(Reporter,on_delete=models.CASCADE)

    notification_type=models.CharField(max_length=20)

    subject=models.CharField(max_length=200)

    message=models.TextField()

    sent_at=models.DateTimeField(auto_now_add=True)

    delivery_status=models.CharField(max_length=30)

    class Meta:
        db_table="notifications"                            


class StatusHistory(models.Model):

    report=models.ForeignKey(Report,on_delete=models.CASCADE)

    old_status=models.ForeignKey(
        ReportStatus,
        on_delete=models.PROTECT,
        related_name="old_status"
    )

    new_status=models.ForeignKey(
        ReportStatus,
        on_delete=models.PROTECT,
        related_name="new_status"
    )

    changed_by=models.ForeignKey(User,on_delete=models.PROTECT)

    changed_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table="status_history"