"""
DemographicsGenerator: Generate synthetic demographic datasets.

This module creates realistic synthetic demographic data for testing,
development, and analytics purposes without using real personal information.
"""

__author__ = 'bchan'
__version__ = '1.0.0'

import argparse
import csv
import logging
import sys
import time
from typing import Dict, List, Optional
from pathlib import Path

import DataMasker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generateDemographics() -> Dict[str, str]:
    """
    Generate a single synthetic demographic record.
    
    Returns:
        Dict[str, str]: A dictionary containing demographic information:
            - ssn: Social Security Number
            - creditCard: Credit card number
            - firstName: First name
            - lastName: Last name
            - address: Street address
            - city: City name
            - state: State abbreviation
            - postalCode: Postal/ZIP code
            - phone: Phone number
            - email: Email address
            
    Example:
        >>> record = generateDemographics()
        >>> 'firstName' in record and 'email' in record
        True
    """
    try:
        member = {}
        
        # Generate identification numbers
        member["ssn"] = DataMasker.generateSSN()
        member['creditCard'] = DataMasker.generateCreditCardNumber()
        
        # Generate name
        name = DataMasker.generateName()
        member['firstName'] = name['firstName']
        member['lastName'] = name['lastName']

        # Generate address
        address = DataMasker.generateAddress()
        member['address'] = address["address"]
        member['city'] = address["city"]
        member['state'] = address["state"]
        member['postalCode'] = address["postalCode"]

        # Generate contact information
        contact = DataMasker.generateContact()
        member["phone"] = contact["phone"]
        member["email"] = contact["email"]

        return member
        
    except Exception as e:
        logger.error(f"Error generating demographics: {e}")
        raise


def generate_batch(records: int) -> List[Dict[str, str]]:
    """
    Generate a batch of synthetic demographic records.
    
    Args:
        records: Number of records to generate.
        
    Returns:
        List[Dict[str, str]]: List of demographic records.
        
    Raises:
        ValueError: If records is not a positive integer.
    """
    if not isinstance(records, int) or records <= 0:
        raise ValueError("Records must be a positive integer")
    
    logger.info(f"Generating {records} demographic records...")
    
    batch = []
    for i in range(records):
        if i % 100 == 0 and i > 0:
            logger.info(f"Generated {i} records...")
        batch.append(generateDemographics())
    
    logger.info(f"Successfully generated {records} records")
    return batch


def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    """
    Save demographic data to a CSV file.
    
    Args:
        data: List of demographic records.
        filename: Output filename.
        
    Raises:
        IOError: If file cannot be written.
        ValueError: If data is empty.
    """
    if not data:
        raise ValueError("No data to save")
    
    try:
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = [
            'ssn', 'creditCard', 'firstName', 'lastName',
            'address', 'city', 'state', 'postalCode', 'email', 'phone'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as outFile:
            writer = csv.DictWriter(outFile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        logger.info(f"Data saved to {output_path}")
        
    except Exception as e:
        logger.error(f"Error saving to file {filename}: {e}")
        raise IOError(f"Failed to save data to {filename}") from e


def main(records: int = 100, output_file: str = 'demographicsData.csv') -> None:
    """
    Main function to generate synthetic demographic data.
    
    Args:
        records: Number of records to generate (default: 100).
        output_file: Output filename (default: 'demographicsData.csv').
        
    Raises:
        Exception: If generation or saving fails.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Starting demographic data generation...")
        logger.info(f"Records to generate: {records}")
        logger.info(f"Output file: {output_file}")
        
        # Generate data
        data = generate_batch(records)
        
        # Save to file
        save_to_csv(data, output_file)
        
        # Calculate and log execution time
        end_time = time.time()
        elapsed = end_time - start_time
        
        logger.info(f"Generation completed successfully!")
        logger.info(f"Execution time: {elapsed:.2f} seconds")
        logger.info(f"Records per second: {records/elapsed:.2f}")
        
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Generate synthetic demographic data for testing and development.'
    )
    
    parser.add_argument(
        '-n', '--records',
        type=int,
        default=100,
        help='Number of records to generate (default: 100)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='demographicsData.csv',
        help='Output CSV filename (default: demographicsData.csv)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_arguments()
        
        # Set logging level based on verbose flag
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Verbose logging enabled")
        
        # Validate arguments
        if args.records <= 0:
            logger.error("Number of records must be positive")
            sys.exit(1)
            
        # Run main function
        main(args.records, args.output)
        
    except KeyboardInterrupt:
        logger.info("Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

