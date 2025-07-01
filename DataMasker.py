"""
DataMasker: Core data masking and synthetic data generation utilities.

This module provides functions for generating realistic fake data to replace
sensitive information while maintaining data relationships and characteristics.
"""

__author__ = 'bchan'
__version__ = '1.0.0'

import datetime
import time
from typing import Dict, Optional, Union
from faker import Faker
from dateutil.parser import parse

# Initialize Faker instance
fake = Faker()


def generate_uuid() -> str:
    """
    Generate a UUID4 string without hyphens in uppercase format.
    
    Returns:
        str: A UUID4 string without hyphens in uppercase.
        
    Example:
        >>> uuid = generate_uuid()
        >>> len(uuid)
        32
    """
    uuid = fake.uuid4()
    return uuid.replace("-", "").upper()


def generateSSN() -> str:
    """
    Generate a fake Social Security Number.
    
    Returns:
        str: A fake SSN in XXX-XX-XXXX format.
        
    Note:
        This generates fake SSNs for testing purposes only.
    """
    return fake.ssn()


def generateCreditCardNumber() -> str:
    """
    Generate a fake credit card number.
    
    Returns:
        str: A fake credit card number.
        
    Note:
        This generates fake credit card numbers for testing purposes only.
    """
    return fake.credit_card_number()


def add_days(startdate: Union[datetime.datetime, str], days: int) -> datetime.datetime:
    """
    Add a specified number of days to a date.
    
    Args:
        startdate: The starting date (datetime object or string).
        days: Number of days to add (can be negative).
        
    Returns:
        datetime.datetime: The new date after adding days.
        
    Raises:
        ValueError: If the date string cannot be parsed.
        TypeError: If startdate is not a datetime or string.
        
    Example:
        >>> from datetime import datetime
        >>> new_date = add_days(datetime(2023, 1, 1), 10)
        >>> new_date.day
        11
    """
    if isinstance(startdate, str):
        try:
            startdate = parse(startdate)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format: {startdate}") from e
    
    if not isinstance(startdate, datetime.datetime):
        raise TypeError("startdate must be a datetime object or date string")
    
    return startdate + datetime.timedelta(days=days)


def generateAddress() -> Dict[str, str]:
    """
    Generate a fake address with separate components.
    
    Returns:
        Dict[str, str]: Dictionary containing address components:
            - address: Street address
            - city: City name
            - state: State abbreviation
            - postalCode: Postal/ZIP code
            
    Example:
        >>> addr = generateAddress()
        >>> 'address' in addr and 'city' in addr
        True
    """
    address = {}
    try:
        fullAddress = fake.address()
        addressParts = fullAddress.splitlines()
        
        if len(addressParts) < 2:
            # Fallback for unexpected address format
            address["address"] = fake.street_address()
            address["city"] = fake.city()
            address["state"] = fake.state_abbr()
            address["postalCode"] = fake.postcode()
        else:
            address["address"] = addressParts[0]
            
            # Parse city, state, zip from second line
            if "," in addressParts[1]:
                cityStateZip = addressParts[1].split(",")
                stateZip = cityStateZip[1].strip().split()
                address["city"] = cityStateZip[0].strip()
                address["state"] = stateZip[0] if stateZip else fake.state_abbr()
                address["postalCode"] = stateZip[1] if len(stateZip) > 1 else fake.postcode()
            else:
                cityStateZip = addressParts[1].split()
                address["city"] = cityStateZip[0] if cityStateZip else fake.city()
                address["state"] = cityStateZip[1] if len(cityStateZip) > 1 else fake.state_abbr()
                address["postalCode"] = cityStateZip[2] if len(cityStateZip) > 2 else fake.postcode()
                
    except Exception as e:
        # Fallback to individual components if parsing fails
        address["address"] = fake.street_address()
        address["city"] = fake.city()
        address["state"] = fake.state_abbr()
        address["postalCode"] = fake.postcode()
        
    return address


def generateName(gender: Optional[str] = None) -> Dict[str, str]:
    """
    Generate a fake name, optionally based on gender.
    
    Args:
        gender: Optional gender specification ('Male' or 'Female').
                If None, generates a random name.
                
    Returns:
        Dict[str, str]: Dictionary containing:
            - firstName: First name
            - lastName: Last name
            
    Example:
        >>> name = generateName('Female')
        >>> 'firstName' in name and 'lastName' in name
        True
    """
    name = {}
    
    try:
        if gender is None:
            name['firstName'] = fake.first_name()
        elif gender.lower() == 'male':
            name['firstName'] = fake.first_name_male()
        elif gender.lower() == 'female':
            name['firstName'] = fake.first_name_female()
        else:
            # Default to random if gender is unrecognized
            name['firstName'] = fake.first_name()
            
        name["lastName"] = fake.last_name()
        
    except Exception as e:
        # Fallback to basic name generation
        name['firstName'] = fake.first_name()
        name["lastName"] = fake.last_name()
        
    return name


def generateContact() -> Dict[str, str]:
    """
    Generate fake contact information.
    
    Returns:
        Dict[str, str]: Dictionary containing:
            - email: Email address
            - phone: Phone number
            
    Example:
        >>> contact = generateContact()
        >>> '@' in contact['email']
        True
    """
    contact = {}
    try:
        contact["email"] = fake.email()
        contact["phone"] = fake.phone_number()
    except Exception as e:
        # Fallback values
        contact["email"] = f"{fake.user_name()}@{fake.domain_name()}"
        contact["phone"] = fake.numerify("###-###-####")
        
    return contact


# Legacy function for backward compatibility
def generateDemographics() -> Dict[str, str]:
    """
    Generate a complete demographic record.
    
    Returns:
        Dict[str, str]: Complete demographic information including
                       name, address, contact info, and identifiers.
                       
    Note:
        This function is deprecated. Use individual functions instead.
    """
    member = {}
    member.update(generateName())
    member.update(generateAddress()) 
    member.update(generateContact())
    member["ssn"] = generateSSN()
    member["creditCard"] = generateCreditCardNumber()
    member["uuid"] = generate_uuid()
    
    return member


if __name__ == "__main__":
    # Example usage
    print("DataMasker Example Output:")
    print("-" * 30)
    
    # Generate sample data
    name = generateName("Female")
    address = generateAddress()
    contact = generateContact()
    
    print(f"Name: {name['firstName']} {name['lastName']}")
    print(f"Address: {address['address']}")
    print(f"City: {address['city']}, {address['state']} {address['postalCode']}")
    print(f"Email: {contact['email']}")
    print(f"Phone: {contact['phone']}")
    print(f"SSN: {generateSSN()}")
    print(f"UUID: {generate_uuid()}")


