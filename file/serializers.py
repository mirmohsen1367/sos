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

from django.core.exceptions import ObjectDoesNotExist


class IndividualInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndividualInformation
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile",
            "national_code",
            "father_name",
            "issue_place",
            "birthdate",
        )


class InsurerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurerInfo
        fields = ("insurer_name", "unique_identifier")

    def validate_insurer_name(self, value):
        insurer = self.context["insurer"]
        if value != insurer:
            raise serializers.ValidationError(
                {"insurer_name": "Please enter valid insurer name."}
            )
        return value

class PolicyHolderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyHolderInfo
        fields = ("policy_holder_name", "unique_identifier")


class PlanInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanInfo
        fields = ("insurance_policy_number", "plan_name", "unique_identifier")


class InsurancePolicySerializer(serializers.ModelSerializer):

    policy_holder_info = PolicyHolderInfoSerializer()
    insurer_info = InsurerInfoSerializer()
    plan_info = PlanInfoSerializer()
    individual_information = IndividualInformationSerializer()

    class Meta:
        model = InsurancePolicy
        fields = (
            "from_date",
            "to_date",
            "verify_date",
            "unique_identifier",
            "policy_holder_info",
            "insurer_info",
            "plan_info",
            "individual_information",
        )

    def validate(self, attrs):
        if attrs["to_date"] <= attrs["from_date"]:
            raise serializers.ValidationError("to_date must be later than from_date.")

        if InsurancePolicy.objects.filter(
            Q(
                from_date__lte=attrs["from_date"],
                to_date__gte=attrs["from_date"],
                individual_information__national_code=attrs["individual_information"][
                    "national_code"
                ],
            )
            | Q(
                from_date__lte=attrs["to_date"],
                to_date__gte=attrs["to_date"],
                individual_information__national_code=attrs["individual_information"][
                    "national_code"
                ],
            )
        ).exists():
            raise serializers.ValidationError(
                "If a person has a contract within the date range, creating any other insurance contract is not possible."
            )

        return attrs

    def create(self, validated_data):
        individual_information_data = {
            "first_name": validated_data["individual_information"]["first_name"],
            "last_name": validated_data["individual_information"]["last_name"],
            "email": validated_data["individual_information"]["email"],
            "mobile": validated_data["individual_information"]["mobile"],
            "national_code": validated_data["individual_information"]["national_code"],
            "birthdate": validated_data["individual_information"]["birthdate"],
            "father_name": (
                validated_data["individual_information"]["father_name"]
                if "father_name" in validated_data["individual_information"]
                else None
            ),
            "issue_place": (
                validated_data["individual_information"]["issue_place"]
                if "issue_place" in validated_data["individual_information"]
                else None
            ),
        }
        insurer_info_data = {
            "insurer_name": validated_data["insurer_info"]["insurer_name"],
            "unique_identifier": validated_data["insurer_info"]["unique_identifier"],
        }

        policy_holder_data = {
            "policy_holder_name": validated_data["policy_holder_info"][
                "policy_holder_name"
            ],
            "unique_identifier": validated_data["policy_holder_info"][
                "unique_identifier"
            ],
        }

        plan_data = {
            "insurance_policy_number": validated_data["plan_info"][
                "insurance_policy_number"
            ],
            "plan_name": validated_data["plan_info"]["plan_name"],
            "unique_identifier": validated_data["plan_info"]["unique_identifier"],
        }

        insurance_policy_data = {
            "from_date": validated_data["from_date"],
            "to_date": validated_data["to_date"],
            "verify_date": (
                validated_data["verify_date"]
                if "verify_date" in validated_data
                else None
            ),
            "unique_identifier": validated_data["unique_identifier"],
        }
        with transaction.atomic():
            individual_information = IndividualInformation.objects.create(
                **individual_information_data
            )

            try:
                insurer_info = InsurerInfo.objects.get(
                    insurer_name=validated_data["insurer_info"]["insurer_name"]
                )
            except ObjectDoesNotExist:
                insurer_info = InsurerInfo.objects.create(**insurer_info_data)

            try:
                policy_holder_info = PolicyHolderInfo.objects.get(
                    policy_holder_name=validated_data["policy_holder_info"][
                        "policy_holder_name"
                    ]
                )
            except ObjectDoesNotExist:
                policy_holder_info = PolicyHolderInfo.objects.create(
                    **policy_holder_data
                )

            plan_info = PlanInfo.objects.create(**plan_data)

            insurance_policy = InsurancePolicy.objects.create(
                **insurance_policy_data,
                insurer_info=insurer_info,
                plan_info=plan_info,
                individual_information=individual_information,
                policy_holder_info=policy_holder_info
            )
            return insurance_policy
