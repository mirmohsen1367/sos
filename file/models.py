from django.db import models
from django.core.validators import RegexValidator
from profiles.models import CustomUser as User


class BaseMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class IndividualInformation(BaseMixin):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="user_individual_info"
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(
        validators=[RegexValidator(regex=r"^09\d{9}$")], max_length=11
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


class Insurer(BaseMixin):
    insurer_name = models.CharField(max_length=3)
    insurer_unique_identifier = models.BigIntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "insurer_info"
        unique_together = ("insurer_name", "insurer_unique_identifier")


class PolicyHolderInfo(BaseMixin):
    policy_holder_name = models.CharField(max_length=30)
    policy_holder_unique_identifier = models.BigIntegerField()
    insurer = models.ForeignKey(to=Insurer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "policy_holder_info"
        unique_together = (
            "policy_holder_name",
            "policy_holder_unique_identifier",
            "insurer",
        )


class InsurancePolicy(BaseMixin):
    insurance_policy_number = models.CharField(max_length=20)
    from_date = models.DateField()
    to_date = models.DateField()
    verify_date = models.DateField(null=True, blank=True)
    insurance_policy_unique_identifier = models.BigIntegerField()
    policy_holder_info = models.ForeignKey(
        to=PolicyHolderInfo,
        on_delete=models.CASCADE,
        related_name="holder_insurance_policied",
    )

    insurer = models.ForeignKey(
        to=Insurer, on_delete=models.CASCADE, related_name="insurer_insurance_policies"
    )

    individual_information = models.ForeignKey(
        to=IndividualInformation,
        related_name="individual_insurance_policies",
        on_delete=models.CASCADE,
    )

    plan_info = models.ForeignKey(
        to="file.planInfo",
        related_name="plan_info_insurance_policy",
        on_delete=models.PROTECT,
    )

    def __str__(self) -> str:
        return f"from_date: {self.from_date.strftime('%Y-%m-%d %H:%M:%S')} to_date: {self.to_date.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        db_table = "insurance_policy"
        unique_together = (
            "insurance_policy_number",
            "insurance_policy_unique_identifier",
            "insurer",
            "policy_holder_info",
        )


class PlanInfo(BaseMixin):
    plan_info_name = models.CharField(max_length=20)
    planinfo_unique_identifier = models.BigIntegerField()
    insurer = models.ForeignKey(
        to=Insurer, on_delete=models.CASCADE, related_name="insurer_plan_info"
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = "plan_info"
        unique_together = unique_together = (
            "plan_info_name",
            "planinfo_unique_identifier",
            "insurer",
        )


class InsuredPerson(BaseMixin):

    insurance_policy = models.ForeignKey(InsurancePolicy,
                                         on_delete=models.CASCADE,
                                         related_name="insured_policy"
                                         )
    individual_information = models.ForeignKey(
        to=IndividualInformation,
        on_delete=models.CASCADE,
        related_name="insured_person",
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(
        validators=[RegexValidator(regex=r"^09\d{9}$")], max_length=11
    )
    issue_place = models.CharField(null=True, blank=True, max_length=30)
    birthdate = models.DateField()
    father_name = models.CharField(null=True, blank=True, max_length=30)
    marital_status = models.CharField(
        max_length=10,
        choices=[("Single", "مجرد"), ("Married", "متأهل")],
        default="Single",
    )
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r"^\d{11}$")],
        null=True,
        blank=True,
    )

    card_number = models.CharField(
        max_length=16,
        validators=[RegexValidator(regex=r"^\d{16}$")],
        null=True,
        blank=True,
    )

    dependents = models.IntegerField(default=0)

    class Meta:
        db_table = "insured_plan"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
