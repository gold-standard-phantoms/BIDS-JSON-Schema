import json
import pytest
import os

from definitions import SRC_ROOT
from jsonschema import Draft7Validator


@pytest.fixture()
def set_test_variables():
    """
    Sets up variables for the unit tests below.
    :return: dictionary of test input variables for the unit tests.
    """
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
        "asl_schema": os.path.join(SRC_ROOT, "resources/schemas/asl_bids_schema.json"),
    }

    return test_variables


def test_valid_data_all_fields_specified(set_test_variables):
    """
    :test_id: ASL-SCHEMA-001
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that a valid structure following exactly the definition set in the json schema gets
    validated correctly.
    :inputs: A dictionary object following exactly the structure defined in the asl schema, with all fields mandatory and
    optional specified.
    :criteria: This test is considered passed if the validation method returns True.
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_full"]

    with open(asl_schema, "rb") as fp:
        print(fp.read())
        schema = json.load(fp)
    with open(asl_valid, "rb") as fp:
        data = json.load(fp)

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is True


def test_valid_data_missing_conditional_field(set_test_variables):
    """
    :test_id: ASL-SCHEMA-002
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that a valid structure following the definition set in the json schema gets validated
    correctly.
    :inputs: A dictionary object following exactly the structure defined in the asl schema but missing a conditional field.
    :criteria: This test is considered passed if the validation method returns True.
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_absent_conditional_field"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is True


def test_valid_data_conditional_type_array(set_test_variables):
    """
    :test_id: ASL-SCHEMA-003
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that a valid structure following the definition set in the json schema gets
    validated correctly.
    :inputs: A dictionary object following largely the structure defined in the asl schema. The twist here is the
    LabelingDuration field is an array instead of a single int, as this is allowed in the schema this should not affect
    the validation.
    :criteria: This test is considered passed if the validation method returns True.
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_labeling_duration_array"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is True


def test_invalid_data_wrong_field_type(set_test_variables):
    """
    :test_id: ASL-SCHEMA-004
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that an invalid structure does not get validated against our schema.
    :inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as an array in the schema is replaced by a single numeric value.
    :criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Should be an array let's replace it with an integer
    data["BackgroundSuppressionPulseTime"] = 16

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_missing_required_key(set_test_variables):
    """
    :test_id: ASL-SCHEMA-005
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that an invalid structure does not get validated against our schema.
    :inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as required in the schema is omitted.
    :criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Let's remove a required key
    data.pop("EchoTime", 0)

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_wrong_type_in_array(set_test_variables):
    """
    :test_id: ASL-SCHEMA-006
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that an invalid structure does not get validated against our schema.
    :inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as an array of numbers in the schema is replaced by an array containing numbers and a string.
    :criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Should be an array of numbers, will put a string in the list
    data["FlipAngles"] = [0, "yeah messing around", 14, 60]

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_unexpected_field_value(set_test_variables):
    """
    :test_id: ASL-SCHEMA-007
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that an invalid structure does not get validated against our schema.
    :inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field whose possible values are set in an enumeration in the schema is set to an unexpected (not part of the
    enumeration) value.
    :criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Value should be part of an enum, but let's fill in an unexpected value
    data["ASLContext"] = "And still the type is right"

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_wrong_array_size(set_test_variables):
    """
    :test_id: ASL-SCHEMA-008
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that an invalid structure does not get validated against our schema.
    :inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as an array in the schema is set to an array of the wrong size.
    :criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Array should have three tuples of two elements each, let's change that
    data["LabelingOrientation"] = [[12, 11], [10, 12], [7, 6], [2, 2]]

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_wrong_internal_array_size(set_test_variables):
    """
    :test_id: ASL-SCHEMA-009
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that an invalid structure does not get validated against our schema.
    :inputs: A dictionary object following largely the structure defined in the asl schema. The 'mistake' here, is that a
    field identified as an array in the schema is set to an array with an inner element of the wrong size.
    :criteria: This test is considered passed if the validation method returns False.
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Array should have three tuples of two elements each, let's change that
    data["LocationOfLabelingPlane"] = [[12, 11], [10, 12], [7, 6, 5]]

    validator = Draft7Validator(schema=schema)
    valid = validator.is_valid(instance=data)

    assert valid is False


def test_invalid_data_multiple_errors(set_test_variables):
    """
    :test_id: ASL-SCHEMA-010
    :req_id: D2N-FUN-REQ-003
    :description: This test verifies that an invalid structure does not get validated against our schema.
    :inputs: A dictionary object following largely the structure defined in the asl schema. The object gathers all the
    mistakes tested previously.
    :criteria: This test is considered passed if the validation method returns False. and the number of errors is
    correctly estimated (6)
    """
    asl_schema = set_test_variables["asl_schema"]
    asl_valid = set_test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

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
