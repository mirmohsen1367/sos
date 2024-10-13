from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import (
    IndividualInformation,
    InsurancePolicy,
    Insurer,
    InsuredPerson,
    PolicyHolderInfo,
    PlanInfo,
)


class IndividualInformationAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "last_name",
        "email",
        "mobile",
        "get_username",
        "national_code",
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request)

    def get_username(self, obj):
        return obj.user.username

    raw_id_fields = ("user",)
    list_display_links = ("national_code",)

    get_username.description = "username"


class InsurerAdmin(admin.ModelAdmin):
    list_display = ["insurer_name", "insurer_unique_identifier"]
    search_fields = ("insurer_name",)


class PolicyHolderInfoAdmin(admin.ModelAdmin):
    list_display = [
        "policy_holder_name",
        "policy_holder_unique_identifier",
        "get_insurer",
    ]
    search_fields = ("policy_holder_name", "insurer__name")
    raw_id_fields = ("insurer",)

    def get_insurer(self, obj):
        return obj.insurer.name

    get_insurer.description = "insurer"


class PlanInfoAdmin(admin.ModelAdmin):
    list_display = ["plan_info_name"]
    list_display_links = ["plan_info_name"]


class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = [
        "insurance_policy_number",
        "get_from_date",
        "get_to_date",
        "insurance_policy_unique_identifier",
        "get_insurer",
        "get_policy_holder_info",
        "get_individual_info",
        "get_plan_info_admin",
    ]

    list_display_links = [
        "get_insurer",
        "insurance_policy_unique_identifier",
        "get_individual_info",
    ]
    raw_id_fields = ("individual_information",)
    list_filter = ("insurer",)

    def get_from_date(self, obj):
        return self.obj.from_date.strftime("%m/%d/%Y")

    get_from_date.description = "from_date"

    def get_to_date(self, obj):
        return self.obj.to_date.strftime("%m/%d/%Y")

    get_to_date.description = "to_date"

    def get_insurer(self, obj):
        return self.obj.insurer.name

    get_insurer.description = "insurer"

    def get_policy_holder_info(self, obj):
        return self.obj.policy_holder_info.name

    get_policy_holder_info.description = "policy_holder_info"

    def get_individual_info(self, obj):
        return self.obj.individual_information.national_code

    get_individual_info.description = "individual_info"

    def get_plan_info_admin(self, obj):
        return self.obj.plan_info.name


class InsuredPersonAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "get_individual_information"]
    search_fields = ("individual_information__national_code",)
    list_display_links = ("get_individual_information",)

    def get_individual_information(self, obj):
        return obj.individual_information.national_code

    get_individual_information.description = "national_code"


admin.site.register(IndividualInformation, IndividualInformationAdmin)
admin.site.register(Insurer, InsurerAdmin)
admin.site.register(PolicyHolderInfo, PolicyHolderInfoAdmin)
admin.site.register(InsurancePolicy, InsurancePolicyAdmin)
admin.site.register(InsuredPerson, InsuredPersonAdmin)
admin.site.register(PlanInfo, PlanInfoAdmin)
