import json
import pytest
import os

from definitions import SRC_ROOT
from jsonschema import Draft7Validator


@pytest.fixture()
def test_variables():
    test_variables = {
        "asl_valid_full": os.path.join(
            SRC_ROOT, "resources/schemas/tests_jsons/asl_valid/test_asl_schema001.json"
        ),
        "asl_valid_absent_conditional_field": os.path.join(
            SRC_ROOT, "resources/schemas/tests_jsons/asl_valid/test_asl_schema002.json"
        ),
        "asl_valid_labeling_duration_array": os.path.join(
            SRC_ROOT, "resources/schemas/tests_jsons/asl_valid/test_asl_schema003.json"
        ),
        "asl_schema": os.path.join(SRC_ROOT, "resources/schemas/asl_schema.json"),
    }

    return test_variables


def test_valid_data_all_fields_specified(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-001
    Description: This tests verify that a valid structure following exactly the definition set in the json schema gets
    validated correctly.
    Inputs: A dictionary object following exactly the structure defined in the asl schema, with all fields mandatory and
    optional specified.
    Passing Criteria: This test is considered passed if the validation method returns True.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is True


def test_valid_data_missing_conditional_field(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-002
    Description: This tests verify that a valid structure following the definition set in the json schema gets validated
    correctly.
    Inputs: A dictionary object following exactly the structure defined in the asl schema but missing a conditional field.
    Passing Criteria: This test is considered passed if the validation method returns True.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_absent_conditional_field"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is True


def test_valid_data_conditional_type_array(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-003
    Description: This tests verify that a valid structure following the definition set in the json schema gets
    validated correctly.
    Inputs: A dictionary object following largely the structure defined in the asl schema. The twist here is the
    LabelingDuration field is an array instead of a single int, as this is allowed in the schema this should not affect
    the validation.
    Passing Criteria: This test is considered passed if the validation method returns True.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_labeling_duration_array"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is True


def test_invalid_data_wrong_field_type(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-004
    Description: This tests verify that an invalid structure does not get validated against our schema.
    Inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as an array in the schema is replaced by a single numeric value.
    Passing Criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    # Mess up data so that the validation fails
    # Should be an array let's replace it with an integer
    data["BackgroundSuppressionPulseTime"] = 16

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_missing_required_key(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-005
    Description: This tests verify that an invalid structure does not get validated against our schema.
    Inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as required in the schema is omitted.
    Passing Criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    # Mess up data so that the validation fails
    # Let's remove a required key
    data.pop("EchoTime", 0)

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_wrong_type_in_array(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-006
    Description: This tests verify that an invalid structure does not get validated against our schema.
    Inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as an array of numbers in the schema is replaced by an array containing numbers and a string.
    Passing Criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    # Mess up data so that the validation fails
    # Should be an array of numbers, will put a string in the list
    data["FlipAngles"] = [0, "yeah messing around", 14, 60]

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_unexpected_field_value(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-007
    Description: This tests verify that an invalid structure does not get validated against our schema.
    Inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field whose possible values are set in an enumeration in the schema is set to an unexpected (not part of the
    enumeration) value.
    Passing Criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    # Mess up data so that the validation fails
    # Value should be part of an enum, but let's fill in an unexpected value
    data["ASLContext"] = "And still the type is right"

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_wrong_array_size(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-008
    Description: This tests verify that an invalid structure does not get validated against our schema.
    Inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as an array in the schema is set to an array of the wrong size.
    Passing Criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    # Mess up data so that the validation fails
    # Array should have three tuples of two elements each, let's change that
    data["LabelingOrientation"] = [[12, 11], [10, 12], [7, 6], [2, 2]]

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_wrong_internal_array_size(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-009
    Description: This tests verify that an invalid structure does not get validated against our schema.
    Inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as an array in the schema is set to an array with an inner element of the wrong size.
    Passing Criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    # Mess up data so that the validation fails
    # Array should have three tuples of two elements each, let's change that
    data["LocationOfLabelingPlane"] = [[12, 11], [10, 12], [7, 6, 5]]

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_multiple_errors(test_variables):
    """
    D2N-FUN-REQ-003
    ASL-SCHEMA-010
    Description: This tests verify that an invalid structure does not get validated against our schema.
    Inputs: A dictionary object following largely the structure defined in the asl schema. The object gathers all the
    mistakes tested previously.
    Passing Criteria: This test is considered passed if the validation method returns False. and the number of errors is
    correctly estimated (6)
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp, encoding="utf-8")
    with open(asl_valid, "r") as fp:
        data = json.load(fp, encoding="utf-8")

    # Mess up data so that the validation fails
    # Let's take all examples from the tests above
    data["LocationOfLabelingPlane"] = [[12, 11], [10, 12], [7, 6, 5]]
    data["LabelingOrientation"] = [[12, 11], [10, 12], [7, 6], [2, 2]]
    data["ASLContext"] = "And still the type is right"
    data["FlipAngles"] = [0, "yeah messing around", 14, 60]
    data["BackgroundSuppressionPulseTime"] = 16
    data.pop("EchoTime", 0)

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False

    error_count = 0
    for error in validator.iter_errors(instance=data):
        error_count += 1

    assert error_count == 6
