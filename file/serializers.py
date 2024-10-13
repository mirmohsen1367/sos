from rest_framework import serializers
from django.core.validators import RegexValidator

from file.models import IndividualInformation, Insurer, PlanInfo, PolicyHolderInfo


class IndividualInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndividualInformation
        exclude = ("user", )


class PolicyHolderInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PolicyHolderInfo
        exclude = ("insurer", )

class PlanInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanInfo
        exclude = ("insurer", )