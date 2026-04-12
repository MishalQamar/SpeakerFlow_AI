from speakerflow_ai.models import Address


def test_address_attributes():
    """
    GIVEN street, city, state, country
    WHEN Address is initialized
    THEN it has attributes with the same values
    """
    address = Address(
        street="Sunny Street 42",
        city="Dublin",
        state="Leinster",
        country="Ireland",
    )

    assert address.street == "Sunny Street 42"
    assert address.city == "Dublin"
    assert address.state == "Leinster"
    assert address.country == "Ireland"
