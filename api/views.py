from rest_framework import viewsets, mixins, serializers, status
from file.serializers import IndividualInformationSerializer, InsurancePolicySerializer
from utils.factory_parse_data import create_new_data
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

REQUIRED_INSURER_FIELDS = {
    "ASI": [
        "first_name",
        "last_name",
        "email",
        "mobile",
        "national_code",
        "birthdate",
        "issue_place",
        "policy_holder_name",
        "from_date",
        "to_date",
        "verify_date" "insurance_policy_number",
        "plan_name",
        "unique_identifier",
    ],
    "HEK": [
        "name",
        "lname",
        "mail",
        "phone",
        "nationality",
        "tavalod",
        "policy_number",
        "azdate",
        "tadate",
        "policy_number",
        "plan",
        "id",
        "pedar",
    ],
    "MEL": [
        "first_name",
        "last_name",
        "email",
        "mobile",
        "national_code",
        "birthdate",
        "issue_place",
        "policy_holder_name",
        "from_date",
        "to_date",
        "insurance_policy_number",
        "plan_name",
        "unique_identifier",
        "father_name",
    ],
}


class CreateIndividualInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = InsurancePolicySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        insurer = request.query_params.get("insurer")
        if insurer is None:
            raise serializers.ValidationError(
                "Please enter insurance name from query params!"
            )
        data = request.data.copy()
        data_list = list(data.keys())
        required_insurer_fields = REQUIRED_INSURER_FIELDS[insurer]

        for k in required_insurer_fields:
            if k not in data_list:
                raise serializers.ValidationError({k: "The field is required"})

        correct_data = create_new_data(insurer=insurer, data=data)
        if not correct_data:
            raise serializers.ValidationError("Your insurer is not valid.")

        serializer = self.serializer_class(
            data=correct_data, context={"insurer": insurer}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
