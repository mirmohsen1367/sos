from .models import (
    IndividualInformation,
    PlanInfo,
    InsurerInfo,
    PolicyHolderInfo,
    InsurancePolicy,
)
from rest_framework import serializers
from django.db.models import Q
from django.db import transaction


class InsurerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurerInfo
        fields = ("insurer_name", "unique_identifier")


class PolicyHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyHolderInfo
        fields = ("policy_holder_name", "unique_identifier")


class PlanInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanInfo
        fields = ("insurance_policy_number", "plan_name", "unique_identifier")


class InsurancePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePolicy
        fields = ("from_date", "to_date", "verify_date", "unique_identifier")

    def validate(self, attrs):
        if attrs["to_date"] <= attrs["from_date"]:
            raise serializers.ValidationError("to_date must be later than from_date.")
        return attrs


class IndividualInformationSerializer(serializers.ModelSerializer):
    policy_holder = PolicyHolderSerializer()
    insurance_policy = InsurancePolicySerializer()
    plan_info = PlanInfoSerializer()
    insurer_info = InsurerInfoSerializer()

    def validate(self, attrs):
        if InsurancePolicy.objects.filter(
            Q(
                from_date__lte=attrs["insurance_policy"]["from_date"],
                to_date__gte=attrs["insurance_policy"]["from_date"],
                individual_info__national_code=attrs["national_code"],
            )
            | Q(
                from_date__lte=attrs["insurance_policy"]["to_date"],
                to_date__gte=attrs["insurance_policy"]["to_date"],
                individual_info__national_code=attrs["national_code"],
            )
        ).exists():
            raise serializers.ValidationError(
                "If a person has a contract within the date range, creating any other insurance contract is not possible."
            )

        if self.insurer_company != attrs["insurer_info"]["insurer_name"]:
            raise serializers.ValidationError("Please send correct insurer name.")

        return super().validate(attrs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context["request"]
        self.insurer_company = request.query_params.get("insurer")

        match self.insurer_company:
            case "HEK":
                ...
            case "MEL":
                # for MEL insurance we set father_name required
                self.fields["father_name"].required = True
            case "ASI":
                ...
            # for other developers to add field required
            # case new_insurer
            case _:
                ...

    def create(self, validated_data):
        with transaction.atomic():
            individual_information_data = {
                "first_name": validated_data["first_name"],
                "last_name": validated_data["last_name"],
                "email": validated_data["email"],
                "mobile": validated_data["mobile"],
                "birthdate": validated_data["birthdate"],
                "national_code": validated_data["national_code"],
                "father_name": validated_data.get("father_name"),
                "issue_place": validated_data.get("issue_place"),
            }

            individual_info = IndividualInformation.objects.create(
                **individual_information_data
            )

            insurer_info_data = {
                "insurer_name": validated_data["insurer_info"]["insurer_name"],
                "unique_identifier": validated_data["insurer_info"][
                    "unique_identifier"
                ],
            }

            policy_holder_Info_data = {
                "policy_holder_name": validated_data["policy_holder"][
                    "policy_holder_name"
                ],
                "unique_identifier": validated_data["policy_holder"][
                    "unique_identifier"
                ],
            }

            insurance_policy_data = {
                "from_date": validated_data["insurance_policy"]["from_date"],
                "to_date": validated_data["insurance_policy"]["to_date"],
                "unique_identifier": validated_data["insurance_policy"][
                    "unique_identifier"
                ],
            }

            plan_info_data = {
                "insurance_policy_number": validated_data["plan_info"][
                    "insurance_policy_number"
                ],
                "plan_name": validated_data["plan_info"]["plan_name"],
                "unique_identifier": validated_data["plan_info"]["unique_identifier"],
            }

            InsurerInfo.objects.create(
                **insurer_info_data, individual_info=individual_info
            )
            PolicyHolderInfo.objects.create(
                **policy_holder_Info_data, individual_info=individual_info
            )
            InsurancePolicy.objects.create(
                **insurance_policy_data, individual_info=individual_info
            )
            PlanInfo.objects.create(**plan_info_data, individual_info=individual_info)
            return individual_info

    class Meta:
        model = IndividualInformation
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "national_code",
            "birthdate",
            "father_name",
            "issue_place",
            "policy_holder",
            "insurance_policy",
            "plan_info",
            "insurer_info",
        ]
