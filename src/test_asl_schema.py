import json
import pytest
from jsonschema import validate


@pytest.fixture()
def test_variables():
    asl_valid_full = "schemas/tests_jsons/asl_valid/test_asl_schema001.json"
    asl_valid_absent_conditional_field = "schemas/tests_jsons/asl_valid/test_asl_schema002.json"
    asl_valid_labeling_duration_array = "schemas/tests_jsons/asl_valid/test_asl_schema003.json"

    asl_schema = "schemas/asl_schema.json"
    return locals()


def test_valid_data_all_fields_specified(test_variables):
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    test = validate(instance=data, schema=schema)
    assert test is None
