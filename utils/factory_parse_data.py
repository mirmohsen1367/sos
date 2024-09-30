from .interface import AbstractParseData


class BaseParseData(AbstractParseData):
    def parse_date(
        self,
        data,
        list_of_key,
    ):
        new_data = {}
        for k, v in data.items():
            if k in list_of_key:
                new_data.update({k: v})
        return new_data

    def create_data(self, data):
        new_data = {}
        individual_info_data = self.parse_date(
            data,
            [
                "first_name",
                "last_name",
                "email",
                "mobile",
                "national_code",
                "birthdate",
                "father_name",
                "issue_place",
            ],
        )

        insurer_info_data = self.parse_date(data, ["insurer_name", "unique_identifier"])
        policy_holder_info_data = self.parse_date(
            data, ["policy_holder_name", "unique_identifier"]
        )
        insurance_policy_data = self.parse_date(
            data, ["from_date", "to_date", "unique_identifier"]
        )
        plan_info_data = self.parse_date(
            data, ["insurance_policy_number", "plan_name", "unique_identifier"]
        )

        individual_info_data.update(
            {
                "policy_holder": policy_holder_info_data,
                "insurance_policy": insurance_policy_data,
                "plan_info": plan_info_data,
                "insurer_info": insurer_info_data,
            }
        )
        new_data.update(individual_info_data)
        return new_data


class InsurerParseHEKData(BaseParseData):
    """
    add maping key and override
    """

    maping_key = {
        "name": "first_name",
        "lname": "last_name",
        "mail": "email",
        "phone": "mobile",
        "nationality": "national_code",
        "birthdate": "birthdate",
        "fathername": "father_name",
        "issueplace": "issue_place",
        "insurer": "insurer_name",
        "policy_holder_name": "policy_holder_name",
        "id": "unique_identifier",
        "azdate": "from_date",
        "tadate": "to_date",
        "policy_number": "insurance_policy_number",
        "plan": "plan_name",
    }

    def parse_date(
        self,
        data,
        list_of_key,
    ):
        new_data = {}
        for k, v in data.items():
            try:
                new_key = self.maping_key[k]
            except KeyError:
                continue
            if k in list_of_key:
                new_data.update({new_key: v})
        return new_data

    def create_data(self, data):
        new_data = {}
        individual_info_data = self.parse_date(
            data,
            [
                "name",
                "lname",
                "mail",
                "phone",
                "nationality",
                "birthdate",
                "fathername",
                "issueplace",
            ],
        )

        insurer_info_data = self.parse_date(data, ["insurer", "id"])
        policy_holder_info_data = self.parse_date(data, ["policy_holder_name", "id"])
        insurance_policy_data = self.parse_date(data, ["azdate", "tadate", "id"])
        plan_info_data = self.parse_date(data, ["policy_number", "plan", "id"])

        individual_info_data.update(
            {
                "policy_holder": policy_holder_info_data,
                "insurance_policy": insurance_policy_data,
                "plan_info": plan_info_data,
                "insurer_info": insurer_info_data,
            }
        )
        new_data.update(individual_info_data)
        return new_data


class InsurerParseMELData(BaseParseData):
    pass


class InsurerParseASIData(BaseParseData):
    pass


def create_new_data(insurer, data):
    match insurer:
        case "MEL":
            return InsurerParseMELData().create_data(data=data)
        case "ASI":
            return InsurerParseASIData().create_data(data=data)
        case "HEK":
            return InsurerParseHEKData().create_data(data=data)

        # for other developer to add new insurer.
        # case new
        case _:
            return
