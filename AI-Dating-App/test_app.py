import pytest
from open_ai import sort_profiles

def test_sort_profiles():
    # Define some sample input data
    user_ID = "ed8c023f-6886-453b-a778-9238fcf979e7"

    # Call the function you want to test
    sorted_profiles = sort_profiles(user_ID)

    # Define the expected output
    expected_sorted_profiles = ['424ce5f1-e976-4663-81e3-52f5b8b77113', 'b4cbf60e-a1ec-44ca-b7ce-98cafa707773', '63246f2c-d6ee-4892-a702-fbc18f81a766']

    # Check if the actual output matches the expected output
    assert sorted_profiles == expected_sorted_profiles
