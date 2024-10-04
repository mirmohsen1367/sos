# from django.contrib import admin
# from file.models import InsurancePolicy


# class InsurancePolicyAdmin(admin.ModelAdmin):
#     list_display = [
#         "get_first_name",
#         "get_last_name",
#         "get_email",
#         "get_mobile",
#         "get_national_code",
#         "get_insurer_name",
#         "get_policy_holder",
#         "get_plan",
#         "get_insurance_policy_number",
#         "get_from_date",
#         "get_to_date",
#     ]

#     search_fields = [
#         "individual_information__national_code",
#         "individual_information__mobile",
#     ]

#     def get_first_name(self, obj):
#         try:
#             return obj.individual_information.first_name
#         except AttributeError:
#             return

#     get_first_name.short_description = "first_name"

#     def get_last_name(self, obj):
#         try:
#             return obj.individual_information.last_name
#         except AttributeError:
#             return

#     get_last_name.short_description = "last_name"

#     def get_email(self, obj):
#         try:
#             return obj.individual_information.email
#         except AttributeError:
#             return

#     get_email.short_description = "email"

#     def get_mobile(self, obj):
#         try:
#             return obj.individual_information.mobile
#         except AttributeError:
#             return

#     get_mobile.short_description = "mobile"

#     def get_national_code(self, obj):
#         try:
#             return obj.individual_information.national_code
#         except AttributeError:
#             return

#     def get_insurer_name(self, obj):
#         try:
#             return obj.insurer_info.insurer_name
#         except AttributeError:
#             return

#     get_insurer_name.short_description = "insurer"

#     def get_policy_holder(self, obj):
#         try:
#             return obj.policy_holder_info.policy_holder_name
#         except AttributeError:
#             return

#     get_policy_holder.short_description = "policy_holder"

#     def get_plan(self, obj):
#         try:
#             return obj.plan_info.get_plan_name_display()
#         except AttributeError:
#             return

#     get_plan.short_description = "plan"

#     def get_insurance_policy_number(self, obj):
#         try:
#             return obj.plan_info.insurance_policy_number
#         except AttributeError:
#             return

#     def get_from_date(self, obj):
#         return obj.from_date.strftime("%Y-%m-%d")

#     get_from_date.short_description = "from_date"

#     def get_to_date(self, obj):
#         return obj.to_date.strftime("%Y-%m-%d")

#     get_to_date.short_description = "to_date"


# admin.site.register(InsurancePolicy, InsurancePolicyAdmin)
