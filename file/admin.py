from django.contrib import admin
from file.models import IndividualInformation


class IndividualInformationAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "mobile",
        "national_code",
        "get_insurer_name",
        "get_policy_holder",
        "get_plan",
        "get_insurance_policy_number",
        "get_from_date",
        "get_to_date",
    ]

    search_fields = ["national_code", "mobile"]

    def get_insurer_name(self, obj):
        try:
            insurer = obj.insurer_info
            return insurer.insurer_name
        except Exception:
            return

    get_insurer_name.short_description = "insurer"

    def get_policy_holder(self, obj):
        try:
            policy = obj.policy_holder
            return policy.policy_holder_name
        except Exception:
            return

    get_policy_holder.short_description = "policy_holder"

    def get_plan(self, obj):
        try:
            plan_info = obj.plan_info
            return plan_info.get_plan_name_display()
        except Exception:
            return

    get_plan.short_description = "plan"

    def get_insurance_policy_number(self, obj):
        try:
            plan_info = obj.plan_info
            return plan_info.insurance_policy_number
        except Exception:
            return

    get_insurance_policy_number.short_description = "insurance_policy_number"

    def get_from_date(self, obj):
        try:
            insurance_policy = obj.insurance_policy
            return insurance_policy.from_date.strftime("%Y-%m-%d")
        except Exception:
            return

    get_from_date.short_description = "from_date"

    def get_to_date(self, obj):
        try:
            insurance_policy = obj.insurance_policy
            return insurance_policy.to_date.strftime("%Y-%m-%d")
        except Exception:
            return

    get_from_date.short_description = "to_date"


admin.site.register(IndividualInformation, IndividualInformationAdmin)
