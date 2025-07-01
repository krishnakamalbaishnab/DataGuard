#!/usr/bin/env python3
"""
Basic tests for DataGuard functionality.

This script provides simple tests to validate that the core DataGuard
functions are working correctly. Run this after installation to verify
everything is functioning properly.
"""

import sys
import traceback
from datetime import datetime
from pathlib import Path

# Add current directory to path to import local modules
sys.path.insert(0, str(Path(__file__).parent))

import DataMasker
import config


class TestResults:
    """Simple test result tracker."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name: str):
        """Record a passing test."""
        self.passed += 1
        print(f"✓ {test_name}")
    
    def add_fail(self, test_name: str, error: str):
        """Record a failing test."""
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"✗ {test_name}: {error}")
    
    def summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\nTest Results: {self.passed}/{total} passed")
        
        if self.failed > 0:
            print(f"\nFailures:")
            for test_name, error in self.errors:
                print(f"  {test_name}: {error}")
        
        return self.failed == 0


def test_basic_functions(results: TestResults):
    """Test basic DataMasker functions."""
    print("\n--- Testing Basic Functions ---")
    
    # Test UUID generation
    try:
        uuid = DataMasker.generate_uuid()
        if isinstance(uuid, str) and len(uuid) == 32:
            results.add_pass("UUID generation")
        else:
            results.add_fail("UUID generation", f"Invalid UUID format: {uuid}")
    except Exception as e:
        results.add_fail("UUID generation", str(e))
    
    # Test SSN generation
    try:
        ssn = DataMasker.generateSSN()
        if isinstance(ssn, str) and len(ssn) > 0:
            results.add_pass("SSN generation")
        else:
            results.add_fail("SSN generation", f"Invalid SSN: {ssn}")
    except Exception as e:
        results.add_fail("SSN generation", str(e))
    
    # Test credit card generation
    try:
        cc = DataMasker.generateCreditCardNumber()
        if isinstance(cc, str) and len(cc) > 0:
            results.add_pass("Credit card generation")
        else:
            results.add_fail("Credit card generation", f"Invalid credit card: {cc}")
    except Exception as e:
        results.add_fail("Credit card generation", str(e))


def test_name_generation(results: TestResults):
    """Test name generation functions."""
    print("\n--- Testing Name Generation ---")
    
    # Test random name
    try:
        name = DataMasker.generateName()
        if 'firstName' in name and 'lastName' in name:
            results.add_pass("Random name generation")
        else:
            results.add_fail("Random name generation", f"Missing fields: {name}")
    except Exception as e:
        results.add_fail("Random name generation", str(e))
    
    # Test male name
    try:
        name = DataMasker.generateName('Male')
        if 'firstName' in name and 'lastName' in name:
            results.add_pass("Male name generation")
        else:
            results.add_fail("Male name generation", f"Missing fields: {name}")
    except Exception as e:
        results.add_fail("Male name generation", str(e))
    
    # Test female name
    try:
        name = DataMasker.generateName('Female')
        if 'firstName' in name and 'lastName' in name:
            results.add_pass("Female name generation")
        else:
            results.add_fail("Female name generation", f"Missing fields: {name}")
    except Exception as e:
        results.add_fail("Female name generation", str(e))
    
    # Test invalid gender (should not crash)
    try:
        name = DataMasker.generateName('Invalid')
        if 'firstName' in name and 'lastName' in name:
            results.add_pass("Invalid gender handling")
        else:
            results.add_fail("Invalid gender handling", f"Missing fields: {name}")
    except Exception as e:
        results.add_fail("Invalid gender handling", str(e))


def test_address_generation(results: TestResults):
    """Test address generation."""
    print("\n--- Testing Address Generation ---")
    
    try:
        address = DataMasker.generateAddress()
        required_fields = ['address', 'city', 'state', 'postalCode']
        
        missing_fields = [field for field in required_fields if field not in address]
        if not missing_fields:
            results.add_pass("Address generation")
        else:
            results.add_fail("Address generation", f"Missing fields: {missing_fields}")
    except Exception as e:
        results.add_fail("Address generation", str(e))


def test_contact_generation(results: TestResults):
    """Test contact information generation."""
    print("\n--- Testing Contact Generation ---")
    
    try:
        contact = DataMasker.generateContact()
        if 'email' in contact and 'phone' in contact:
            # Basic email validation
            if '@' in contact['email']:
                results.add_pass("Contact generation")
            else:
                results.add_fail("Contact generation", f"Invalid email: {contact['email']}")
        else:
            results.add_fail("Contact generation", f"Missing fields: {contact}")
    except Exception as e:
        results.add_fail("Contact generation", str(e))


def test_date_operations(results: TestResults):
    """Test date manipulation functions."""
    print("\n--- Testing Date Operations ---")
    
    # Test with datetime object
    try:
        original = datetime(2023, 1, 1)
        shifted = DataMasker.add_days(original, 10)
        
        if shifted.year == 2023 and shifted.month == 1 and shifted.day == 11:
            results.add_pass("Date shifting (datetime)")
        else:
            results.add_fail("Date shifting (datetime)", f"Unexpected result: {shifted}")
    except Exception as e:
        results.add_fail("Date shifting (datetime)", str(e))
    
    # Test with string input
    try:
        shifted = DataMasker.add_days("2023-01-01", 5)
        if shifted.year == 2023 and shifted.month == 1 and shifted.day == 6:
            results.add_pass("Date shifting (string)")
        else:
            results.add_fail("Date shifting (string)", f"Unexpected result: {shifted}")
    except Exception as e:
        results.add_fail("Date shifting (string)", str(e))
    
    # Test invalid date string
    try:
        DataMasker.add_days("invalid-date", 5)
        results.add_fail("Invalid date handling", "Should have raised an exception")
    except ValueError:
        results.add_pass("Invalid date handling")
    except Exception as e:
        results.add_fail("Invalid date handling", f"Unexpected exception: {e}")


def test_complete_demographics(results: TestResults):
    """Test complete demographic record generation."""
    print("\n--- Testing Complete Demographics ---")
    
    try:
        record = DataMasker.generateDemographics()
        
        expected_fields = [
            'firstName', 'lastName', 'address', 'city', 'state', 
            'postalCode', 'email', 'phone', 'ssn', 'creditCard', 'uuid'
        ]
        
        missing_fields = [field for field in expected_fields if field not in record]
        if not missing_fields:
            results.add_pass("Complete demographics generation")
        else:
            results.add_fail("Complete demographics generation", f"Missing fields: {missing_fields}")
    except Exception as e:
        results.add_fail("Complete demographics generation", str(e))


def test_configuration(results: TestResults):
    """Test configuration functionality."""
    print("\n--- Testing Configuration ---")
    
    # Test config loading
    try:
        effective_config = config.get_effective_config()
        if isinstance(effective_config, dict) and len(effective_config) > 0:
            results.add_pass("Configuration loading")
        else:
            results.add_fail("Configuration loading", "Empty or invalid config")
    except Exception as e:
        results.add_fail("Configuration loading", str(e))
    
    # Test config validation
    try:
        issues = config.validate_config()
        if isinstance(issues, dict):
            results.add_pass("Configuration validation")
        else:
            results.add_fail("Configuration validation", "Invalid validation result")
    except Exception as e:
        results.add_fail("Configuration validation", str(e))


def test_performance(results: TestResults):
    """Test basic performance characteristics."""
    print("\n--- Testing Performance ---")
    
    import time
    
    try:
        start_time = time.time()
        
        # Generate 100 records
        records = []
        for i in range(100):
            records.append(DataMasker.generateDemographics())
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        if elapsed < 10.0:  # Should complete within 10 seconds
            rate = len(records) / elapsed
            results.add_pass(f"Performance test (100 records in {elapsed:.2f}s, {rate:.1f} rec/s)")
        else:
            results.add_fail("Performance test", f"Too slow: {elapsed:.2f} seconds for 100 records")
    except Exception as e:
        results.add_fail("Performance test", str(e))


def main():
    """Run all tests."""
    print("DataGuard Basic Test Suite")
    print("=" * 50)
    print("Testing core functionality...")
    
    results = TestResults()
    
    try:
        test_basic_functions(results)
        test_name_generation(results)
        test_address_generation(results)
        test_contact_generation(results)
        test_date_operations(results)
        test_complete_demographics(results)
        test_configuration(results)
        test_performance(results)
        
        # Print summary
        success = results.summary()
        
        if success:
            print("\n🎉 All tests passed! DataGuard is functioning correctly.")
            return 0
        else:
            print("\n❌ Some tests failed. Check the output above for details.")
            return 1
            
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main()) 