import json
import pytest
from jsonschema import validate, ValidationError


@pytest.fixture()
def test_variables():
    asl_valid_full = "schemas/tests_jsons/asl_valid/test_asl_schema001.json"
    asl_valid_absent_conditional_field = "schemas/tests_jsons/asl_valid/test_asl_schema002.json"
    asl_valid_labeling_duration_array = "schemas/tests_jsons/asl_valid/test_asl_schema003.json"

    asl_schema = "schemas/asl_schema.json"
    return locals()


def test_valid_data_all_fields_specified(test_variables):
    """
    D2N-FUN-REQ-003
    ASL_SCHEMA_001
    Description: This tests verify that a valid structure following exactly the definition set in the json schema gets
    validated correctly.
    Passing Criteria: This test is considered passed if the validation method does not raise any exception.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    test = validate(instance=data, schema=schema)
    assert test is None


def test_valid_data_missing_conditional_field(test_variables):
    """
    D2N-FUN-REQ-003
    ASL_SCHEMA_002
    Description: This tests verify that a valid structure following the definition set in the json schema gets but
    missing a conditional field gets validated correctly.
    Passing Criteria: This test is considered passed if the validation method does not raise any exception.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_absent_conditional_field"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    test = validate(instance=data, schema=schema)
    assert test is None


def test_valid_data_conditional_type_array(test_variables):
    """
    D2N-FUN-REQ-003
    ASL_SCHEMA_003
    Description: This tests verify that a valid structure following the definition set in the json schema gets
    validated correctly. The twist here is the LabelingDuration field is an array instead of a single int, as this is
    allowed in the schema this should not affect the validation.
    Passing Criteria: This test is considered passed if the validation method does not raise any exception.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_labeling_duration_array"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    test = validate(instance=data, schema=schema)
    assert test is None


def test_invalid_data_wrong_field_type(test_variables):
    """
    D2N-FUN-REQ-003
    ASL_SCHEMA_004
    Description: This tests verify that an invalid structure does not get validated against our schema. The 'mistake'
    here, is that a field identified as an array in the schema is replaced by a single numeric value.
    Passing Criteria: This test is considered passed if the validation method raises the ValidationError exception.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_full"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Should be an array let's replace it with an integer
    data["BackgroundSuppressionPulseTime"] = 16

    with pytest.raises(ValidationError):
        validate(instance=data, schema=schema)


def test_invalid_data_missing_required_key(test_variables):
    """
    D2N-FUN-REQ-003
    ASL_SCHEMA_005
    Description: This tests verify that an invalid structure does not get validated against our schema. The 'mistake'
    here, is that a field identified as required in the schema is omitted.
    Passing Criteria: This test is considered passed if the validation method raises the ValidationError exception.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_labeling_duration_array"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Let's remove a required key
    data.pop("EchoTime", 0)

    with pytest.raises(ValidationError):
        validate(instance=data, schema=schema)


def test_invalid_data_wrong_type_in_array(test_variables):
    """
    D2N-FUN-REQ-003
    ASL_SCHEMA_006
    Description: This tests verify that an invalid structure does not get validated against our schema. The 'mistake'
    here, is that a field identified as an array of numbers in the schema is replaced by an array containing numbers and
    a string.
    Passing Criteria: This test is considered passed if the validation method raises the ValidationError exception.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_labeling_duration_array"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Should be an array of numbers, will put a string in the list
    data["FlipAngles"] = [0, "yeah messing around", 14, 60]

    with pytest.raises(ValidationError):
        validate(instance=data, schema=schema)


def test_invalid_data_unexpected_field_value(test_variables):
    """
    D2N-FUN-REQ-003
    ASL_SCHEMA_007
    Description: This tests verify that an invalid structure does not get validated against our schema. The 'mistake'
    here, is that a field whose possible values are set in an enumeration in the schema is set to an unexpected (not
    part of the enumeration) value.
    Passing Criteria: This test is considered passed if the validation method raises the ValidationError exception.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_labeling_duration_array"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Value should be part of an enum, but let's fill in an unexpected value
    data["ASLContext"] = "And still the type is right"

    with pytest.raises(ValidationError):
        validate(instance=data, schema=schema)


def test_invalid_data_wrong_array_size(test_variables):
    """
    D2N-FUN-REQ-003
    ASL_SCHEMA_008
    Description: This tests verify that an invalid structure does not get validated against our schema. The 'mistake'
    here, is that a field identified as an array in the schema is set to an array of the wrong size.
    Passing Criteria: This test is considered passed if the validation method raises the ValidationError exception.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_labeling_duration_array"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Array should have three tuples of two elements each, let's change that
    data["LabelingOrientation"] = [[12, 11], [10, 12], [7, 6], [2, 2]]

    with pytest.raises(ValidationError):
        validate(instance=data, schema=schema)


def test_invalid_data_wrong_internal_array_size(test_variables):
    """
    D2N-FUN-REQ-003
    ASL_SCHEMA_009
    Description: This tests verify that an invalid structure does not get validated against our schema. The 'mistake'
    here, is that a field identified as an array in the schema is set to an array with an inner element of the wrong
    size.
    Passing Criteria: This test is considered passed if the validation method raises the ValidationError exception.
    """
    asl_schema = test_variables["asl_schema"]
    asl_valid = test_variables["asl_valid_labeling_duration_array"]

    with open(asl_schema, "r") as fp:
        schema = json.load(fp)
    with open(asl_valid, "r") as fp:
        data = json.load(fp)

    # Mess up data so that the validation fails
    # Array should have three tuples of two elements each, let's change that
    data["LocationOfLabelingPlane"] = [[12, 11], [10, 12], [7, 6, 5]]

    with pytest.raises(ValidationError):
        validate(instance=data, schema=schema)
