from file.models import (PolicyHolderInfo, InsurerInfo,
                         IndividualInformation, PlanInfo)
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_MEL_insurance(client, user):
    # create_individual_info without login
    data = {
        "first_name": "admin",
        "last_name": "admin",
        "email": "email@gmail.com",
        "mobile": "09123431112",
        "national_code": "1234567811",
        "birthdate": "1990-10-02",
        "father_name": "admin",
        "issue_place": "test",
        "unique_identifier": "123",
        "policy_holder_name": "test",
        "plan_name": "silver_plan",
        "insurance_policy_number": "123",
        "insurer_name": "MEL",
        "from_date": "2021-10-09",
        "to_date": "2022-10-03",
    }

    url = reverse("create-individual-info-list")
    url_with_params = f"{url}?insurer=MEL"
    create_individual_info_api = client.post(url_with_params, data)
    assert create_individual_info_api.status_code == 401

    # get jwt token
    token_api = client.post(
        reverse("token_obtain_pair"), {"username": user.username, "password": "admin"}
    )
    assert token_api.status_code == 200
    token = token_api.json()["access"]

    # test again with token
    client.credentials(HTTP_AUTHORIZATION="jwt " + token)
    create_individual_info_api = client.post(url_with_params, data)
    # create insurer data
    assert create_individual_info_api.status_code == 201
    assert IndividualInformation.objects.all().count() == 1
    assert InsurerInfo.objects.all().count() == 1
    assert PolicyHolderInfo.objects.all().count() == 1
    assert PlanInfo.objects.all().count() == 1

    # create with duplicate unique_identifier
    create_individual_info_api = client.post(url_with_params, data)
    create_individual_info_api.status_code == 400

    # create with overlap form_date and end_date
    data = {
        "first_name": "admin",
        "last_name": "admin",
        "email": "email@gmail.com",
        "mobile": "09123431112",
        "national_code": "1234567811",
        "birthdate": "1990-10-02",
        "father_name": "admin",
        "issue_place": "test",
        "unique_identifier": "1234",
        "policy_holder_name": "test",
        "plan_name": "silver_plan",
        "insurance_policy_number": "123",
        "insurer_name": "MEL",
        "from_date": "2020-10-09",
        "to_date": "2022-10-03",
    }

    create_individual_info_api = client.post(url_with_params, data)
    assert (
        create_individual_info_api.json()["non_field_errors"][0]
        == "If a person has a contract within the date range, creating any other insurance contract is not possible."
    )
    assert create_individual_info_api.status_code == 400

    # for other person and other nationsal code

    data = {
        "first_name": "admin",
        "last_name": "admin",
        "email": "email@gmail.com",
        "mobile": "09123431112",
        "national_code": "1234567812",
        "birthdate": "1990-10-02",
        "father_name": "admin",
        "issue_place": "test",
        "unique_identifier": "1234",
        "policy_holder_name": "test",
        "plan_name": "silver_plan",
        "insurance_policy_number": "123",
        "insurer_name": "MEL",
        "from_date": "2020-10-09",
        "to_date": "2022-10-03",
    }

    create_individual_info_api = client.post(url_with_params, data)
    # create insurer data
    assert create_individual_info_api.status_code == 201
    assert IndividualInformation.objects.all().count() == 2
    assert InsurerInfo.objects.all().count() == 1
    assert PolicyHolderInfo.objects.all().count() == 1
    assert PlanInfo.objects.all().count() == 2


@pytest.mark.django_db
def test_HEK_insurance(client, user):
     # get jwt token
    token_api = client.post(
        reverse("token_obtain_pair"), {"username": user.username, "password": "admin"}
    )
    assert token_api.status_code == 200
    token = token_api.json()["access"]

    # test again with token
    client.credentials(HTTP_AUTHORIZATION="jwt " + token)
    # test like mellat data
    data = {
        "first_name": "admin",
        "last_name": "admin",
        "email": "email@gmail.com",
        "mobile": "09123431112",
        "national_code": "1234567812",
        "birthdate": "1990-10-02",
        "father_name": "admin",
        "issue_place": "test",
        "unique_identifier": "1234",
        "policy_holder_name": "test",
        "plan_name": "silver_plan",
        "insurance_policy_number": "123",
        "insurer_name": "HEK",
        "from_date": "2020-10-09",
        "to_date": "2022-10-03",
    }

    url = reverse("create-individual-info-list")
    url_with_params = f"{url}?insurer=HEK"
    create_individual_info_api = client.post(url_with_params, data)
    assert create_individual_info_api.status_code == 400

    data = {
        "name": "admin",
        "lname": "admin",
        "mail": "email@gmail.com",
        "phone": "09123431112",
        "nationality": "1234567812",
        "tavalod": "1990-10-02",
        "pedar": "admin",
        "issueplace": "test",
        "id": "1234",
        "policy_holder_name": "test",
        "plan": "silver_plan",
        "policy_number": "123",
        "insurer": "HEK",
        "azdate": "2020-10-09",
        "tadate": "2022-10-03",
    }
    
    create_individual_info_api = client.post(url_with_params, data)
    assert create_individual_info_api.status_code == 201
    assert create_individual_info_api.status_code == 201
    assert IndividualInformation.objects.all().count() == 1
    assert InsurerInfo.objects.all().count() == 1
    assert PolicyHolderInfo.objects.all().count() == 1
    assert PlanInfo.objects.all().count() == 1

@pytest.mark.skip(reason="For other developer create test on asi insurance.")
def test_ASI_insurance(client, user):
    pass
