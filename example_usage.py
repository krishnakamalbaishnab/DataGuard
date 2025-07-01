#!/usr/bin/env python3
"""
DataGuard Example Usage.

This script demonstrates various ways to use the DataGuard toolkit
for data masking and synthetic data generation.
"""

import sys
from pathlib import Path

# Add current directory to path to import local modules
sys.path.insert(0, str(Path(__file__).parent))

import DataMasker
import config


def example_basic_usage():
    """Demonstrate basic data generation functions."""
    print("=" * 60)
    print("BASIC DATA GENERATION EXAMPLES")
    print("=" * 60)
    
    # Generate individual components
    print("1. Individual Data Components:")
    print("-" * 30)
    
    name = DataMasker.generateName('Female')
    print(f"Female Name: {name['firstName']} {name['lastName']}")
    
    name = DataMasker.generateName('Male')
    print(f"Male Name: {name['firstName']} {name['lastName']}")
    
    address = DataMasker.generateAddress()
    print(f"Address: {address['address']}")
    print(f"Location: {address['city']}, {address['state']} {address['postalCode']}")
    
    contact = DataMasker.generateContact()
    print(f"Email: {contact['email']}")
    print(f"Phone: {contact['phone']}")
    
    # Generate identification numbers
    print(f"\nSSN: {DataMasker.generateSSN()}")
    print(f"Credit Card: {DataMasker.generateCreditCardNumber()}")
    print(f"UUID: {DataMasker.generate_uuid()}")


def example_complete_records():
    """Demonstrate generating complete demographic records."""
    print("\n" + "=" * 60)
    print("COMPLETE DEMOGRAPHIC RECORDS")
    print("=" * 60)
    
    print("Generating 3 complete demographic records:")
    print("-" * 50)
    
    for i in range(3):
        record = DataMasker.generateDemographics()
        print(f"\nRecord {i + 1}:")
        for key, value in record.items():
            print(f"  {key:12}: {value}")


def example_date_operations():
    """Demonstrate date shifting operations."""
    print("\n" + "=" * 60)
    print("DATE OPERATIONS")
    print("=" * 60)
    
    from datetime import datetime
    
    original_date = datetime(1990, 1, 15)
    print(f"Original date: {original_date.strftime('%Y-%m-%d')}")
    
    # Shift forward
    shifted_forward = DataMasker.add_days(original_date, 10)
    print(f"Shifted +10 days: {shifted_forward.strftime('%Y-%m-%d')}")
    
    # Shift backward
    shifted_backward = DataMasker.add_days(original_date, -5)
    print(f"Shifted -5 days: {shifted_backward.strftime('%Y-%m-%d')}")
    
    # Shift with string input
    shifted_string = DataMasker.add_days("1990-01-15", 20)
    print(f"From string +20 days: {shifted_string.strftime('%Y-%m-%d')}")


def example_batch_generation():
    """Demonstrate batch data generation."""
    print("\n" + "=" * 60)
    print("BATCH DATA GENERATION")
    print("=" * 60)
    
    import time
    
    print("Generating 50 records in batch...")
    start_time = time.time()
    
    records = []
    for i in range(50):
        records.append(DataMasker.generateDemographics())
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"Generated {len(records)} records in {elapsed:.3f} seconds")
    print(f"Rate: {len(records)/elapsed:.1f} records/second")
    
    # Show first few records
    print(f"\nFirst 3 records:")
    for i, record in enumerate(records[:3]):
        print(f"  {i+1}. {record['firstName']} {record['lastName']} - {record['email']}")


def example_error_handling():
    """Demonstrate error handling and edge cases."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING EXAMPLES")
    print("=" * 60)
    
    # Test invalid date
    print("1. Testing invalid date handling:")
    try:
        result = DataMasker.add_days("invalid-date", 10)
        print(f"  Result: {result}")
    except ValueError as e:
        print(f"  ✓ Caught expected error: {e}")
    
    # Test invalid gender
    print("\n2. Testing invalid gender (should default gracefully):")
    name = DataMasker.generateName("Unknown")
    print(f"  Generated name with invalid gender: {name['firstName']} {name['lastName']}")
    
    # Test empty/None inputs
    print("\n3. Testing None gender (should work fine):")
    name = DataMasker.generateName(None)
    print(f"  Generated name with None gender: {name['firstName']} {name['lastName']}")


def example_configuration():
    """Demonstrate configuration usage."""
    print("\n" + "=" * 60)
    print("CONFIGURATION EXAMPLES")
    print("=" * 60)
    
    print("Current configuration settings:")
    print("-" * 30)
    
    effective_config = config.get_effective_config()
    for key, value in effective_config.items():
        print(f"  {key:15}: {value}")
    
    print(f"\nDefault field names:")
    print(f"  Generated: {config.GENERATED_FIELDS}")
    print(f"  Masked: {config.MASKED_FIELDS}")
    
    print(f"\nSensitive fields (hidden from logs): {config.SENSITIVE_FIELDS}")


def example_advanced_usage():
    """Demonstrate advanced usage patterns."""
    print("\n" + "=" * 60)
    print("ADVANCED USAGE PATTERNS")
    print("=" * 60)
    
    # Generate data matching specific patterns
    print("1. Generate matching demographic pairs:")
    print("-" * 40)
    
    # Family simulation - same last name, same address
    family_name = DataMasker.generateName('Male')['lastName']
    family_address = DataMasker.generateAddress()
    
    for i, gender in enumerate(['Male', 'Female']):
        name = DataMasker.generateName(gender)
        contact = DataMasker.generateContact()
        
        print(f"  Family Member {i+1}:")
        print(f"    Name: {name['firstName']} {family_name}")
        print(f"    Address: {family_address['address']}")
        print(f"    Email: {contact['email']}")
    
    print("\n2. Generate data for different locales:")
    print("-" * 40)
    
    # Note: This would require Faker with different locales
    print("  Current locale: en_US (modify config.FAKER_LOCALE to change)")
    
    name_us = DataMasker.generateName()
    print(f"  US-style name: {name_us['firstName']} {name_us['lastName']}")


def main():
    """Run all examples."""
    print("DataGuard Toolkit - Usage Examples")
    print("This script demonstrates various features of the DataGuard toolkit.")
    print("Run this script to see examples of data generation and masking.")
    
    try:
        example_basic_usage()
        example_complete_records()
        example_date_operations()
        example_batch_generation()
        example_error_handling()
        example_configuration()
        example_advanced_usage()
        
        print("\n" + "=" * 60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nTo use DataGuard in your projects:")
        print("  1. Import the modules: import DataMasker")
        print("  2. Use DemographicsGenerator.py to create synthetic data")
        print("  3. Use DemographicsMasking.py to mask existing data")
        print("  4. Customize behavior by modifying config.py")
        print("\nFor command-line usage:")
        print("  python DemographicsGenerator.py --help")
        print("  python DemographicsMasking.py --help")
        
    except Exception as e:
        print(f"\n❌ Error during examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 