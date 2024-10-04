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
    name = models.CharField(max_length=3)
    unique_identifier = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return self.insurer_name

    class Meta:
        db_table = "insurer_info"
        unique_together = ("name", "unique_identifier")


class PolicyHolderInfo(BaseMixin):
    name = models.CharField(max_length=30)
    unique_identifier = models.BigIntegerField(unique=True)
    insurer = models.ForeignKey(to=Insurer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.policy_holder_name

    class Meta:
        db_table = "policy_holder_info"
        unique_together = ("name", "unique_identifier", "insurer")


class InsurancePolicy(BaseMixin):
    number = models.CharField(max_length=20)
    from_date = models.DateField()
    to_date = models.DateField()
    verify_date = models.DateField(null=True, blank=True)
    unique_identifier = models.BigIntegerField(unique=True)
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

    def __str__(self) -> str:
        return f"from_date: {self.from_date.strftime('%Y-%m-%d %H:%M:%S')} to_date: {self.to_date.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        db_table = "insurance_policy"
        unique_together = ("number", "unique_identifier", "insurer")


class PlanInfo(BaseMixin):
    insurance_policy = models.OneToOneField(
        to=InsurancePolicy, related_name="plan_info", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=20)
    unique_identifier = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.plan_name}"

    class Meta:
        db_table = "plan_info"
        unique_together = ("name", "unique_identifier")


class InsuredPerson(BaseMixin):
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
