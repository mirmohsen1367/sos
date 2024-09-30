from django.db import models
from django.core.validators import RegexValidator


class BaseMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class IndividualInformation(BaseMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(
        validators=[RegexValidator(regex=r"^09\d{9}$")],
        max_length=11,
    )
    national_code = models.CharField(
        max_length=10, validators=[RegexValidator(regex=r"^\d{10}$")]
    )
    birthdate = models.DateField()
    father_name = models.CharField(null=True, blank=True, max_length=30)
    issue_place = models.CharField(null=True, blank=True, max_length=30)

    def __str__(self) -> str:
        return f"{self.first_name} f{self.last_name}"

    class Meta:
        db_table = "individual_information"


class InsurerInfo(BaseMixin):
    INSURER = (("MEL", "ملت"), ("ASI", "آسیا"), ("HEK", "حکمت"))
    insurer_name = models.CharField(max_length=3, choices=INSURER)
    unique_identifier = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.insurer_name

    class Meta:
        db_table = "insurer_info"
        unique_together = ("insurer_name", "unique_identifier")


class PolicyHolderInfo(BaseMixin):
    policy_holder_name = models.CharField(max_length=30)
    unique_identifier = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.policy_holder_name

    class Meta:
        db_table = "policy_holder_info"
        unique_together = ("policy_holder_name", "unique_identifier")


class InsurancePolicy(BaseMixin):
    """
    مشخصات بیمه نامه
    """

    from_date = models.DateField()
    to_date = models.DateField()
    verify_date = models.DateField(null=True, blank=True)
    unique_identifier = models.CharField(max_length=20, unique=True)
    policy_holder_info = models.ForeignKey(
        to=PolicyHolderInfo,
        on_delete=models.PROTECT,
        related_name="holder_insurance_policy",
    )
    insurer_info = models.ForeignKey(
        to=InsurerInfo,
        on_delete=models.CASCADE,
        related_name="insurer_insurance_policy",
    )

    plan_info = models.OneToOneField(
        to="file.PlanInfo",
        related_name="plan_insurance_policy",
        on_delete=models.PROTECT,
    )

    individual_information = models.OneToOneField(
        to=IndividualInformation,
        related_name="individual_insurance_policy",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"from_date: {self.from_date.strftime('%Y-%m-%d %H:%M:%S')} to_date: {self.to_date.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        db_table = "insurance_policy"


class PlanInfo(BaseMixin):
    PLAN = (("silver_plan", "طرح نقره ایی"), ("golden_plan", "طرح طلایی"))
    insurance_policy_number = models.CharField(max_length=20)
    plan_name = models.CharField(choices=PLAN, max_length=20)
    unique_identifier = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.insurance_policy_number} {self.plan_name}"

    class Meta:
        db_table = "plan_info"
        unique_together = ("insurance_policy_number", "unique_identifier")
