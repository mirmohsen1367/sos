from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

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
    # serializer_class = InsurancePolicySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        pass
