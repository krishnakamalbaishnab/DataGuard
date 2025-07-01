"""
DemographicsMasking: Mask sensitive data in existing demographic datasets.

This module reads existing demographic data and replaces sensitive information
with realistic fake data while preserving certain characteristics and relationships.
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
from dateutil.parser import parse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def mask_demographic_record(input_record: Dict[str, str], date_shift_days: int = 10) -> Dict[str, str]:
    """
    Mask a single demographic record while preserving certain characteristics.
    
    Args:
        input_record: Original demographic record from CSV.
        date_shift_days: Number of days to shift birth dates (default: 10).
        
    Returns:
        Dict[str, str]: Masked demographic record with fake data.
        
    Raises:
        ValueError: If required fields are missing or invalid.
        
    Example:
        >>> original = {'birthDate': '01-01-1990', 'gender': 'Male', 'firstName': 'John'}
        >>> masked = mask_demographic_record(original)
        >>> masked['gender'] == 'Male'  # Gender preserved
        True
    """
    try:
        masked_record = {}
        
        # Generate new SSN
        masked_record["ssn"] = DataMasker.generateSSN()
        
        # Handle birth date with configurable shift
        if 'birthDate' in input_record and input_record['birthDate']:
            try:
                birth_date = parse(input_record["birthDate"])
                shifted_date = DataMasker.add_days(birth_date, date_shift_days)
                masked_record['birthDate'] = shifted_date.strftime('%m-%d-%Y')
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid birth date '{input_record['birthDate']}', using original: {e}")
                masked_record['birthDate'] = input_record.get('birthDate', '')
        else:
            masked_record['birthDate'] = ''

        # Preserve gender but generate appropriate name
        gender = input_record.get('gender', '').strip()
        masked_record['gender'] = gender
        
        name = DataMasker.generateName(gender if gender else None)
        masked_record['firstName'] = name['firstName']
        masked_record['lastName'] = name['lastName']

        # Generate new address
        address = DataMasker.generateAddress()
        masked_record['address'] = address["address"]
        masked_record['city'] = address["city"]
        masked_record['state'] = address["state"]
        masked_record['postalCode'] = address["postalCode"]

        # Generate new contact information
        contact = DataMasker.generateContact()
        masked_record["phone"] = contact["phone"]
        masked_record["email"] = contact["email"]

        return masked_record
        
    except Exception as e:
        logger.error(f"Error masking record: {e}")
        logger.debug(f"Input record: {input_record}")
        raise


def load_demographics_data(filename: str) -> List[Dict[str, str]]:
    """
    Load demographic data from a CSV file.
    
    Args:
        filename: Path to the input CSV file.
        
    Returns:
        List[Dict[str, str]]: List of demographic records.
        
    Raises:
        FileNotFoundError: If input file doesn't exist.
        IOError: If file cannot be read.
        ValueError: If file is empty or malformed.
    """
    input_path = Path(filename)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {filename}")
    
    try:
        data = []
        with open(input_path, 'r', encoding='utf-8') as inFile:
            reader = csv.DictReader(inFile)
            
            if not reader.fieldnames:
                raise ValueError("CSV file appears to be empty or has no headers")
            
            logger.info(f"CSV columns found: {list(reader.fieldnames)}")
            
            for row_num, row in enumerate(reader, 1):
                if any(row.values()):  # Skip completely empty rows
                    data.append(row)
                else:
                    logger.warning(f"Skipping empty row {row_num}")
        
        if not data:
            raise ValueError("No valid data rows found in CSV file")
            
        logger.info(f"Loaded {len(data)} records from {filename}")
        return data
        
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        raise IOError(f"Failed to load data from {filename}") from e


def save_masked_data(data: List[Dict[str, str]], filename: str) -> None:
    """
    Save masked demographic data to a CSV file.
    
    Args:
        data: List of masked demographic records.
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
            'ssn', 'birthDate', 'gender', 'firstName', 'lastName',
            'address', 'city', 'state', 'postalCode', 'email', 'phone'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as outFile:
            writer = csv.DictWriter(outFile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        logger.info(f"Masked data saved to {output_path}")
        
    except Exception as e:
        logger.error(f"Error saving to file {filename}: {e}")
        raise IOError(f"Failed to save masked data to {filename}") from e


def mask_demographics_batch(
    input_data: List[Dict[str, str]], 
    date_shift_days: int = 10
) -> List[Dict[str, str]]:
    """
    Mask a batch of demographic records.
    
    Args:
        input_data: List of original demographic records.
        date_shift_days: Number of days to shift birth dates.
        
    Returns:
        List[Dict[str, str]]: List of masked demographic records.
    """
    logger.info(f"Masking {len(input_data)} records with {date_shift_days}-day date shift...")
    
    masked_data = []
    errors = 0
    
    for i, record in enumerate(input_data):
        try:
            if i % 100 == 0 and i > 0:
                logger.info(f"Masked {i} records...")
                
            masked_record = mask_demographic_record(record, date_shift_days)
            masked_data.append(masked_record)
            
        except Exception as e:
            logger.error(f"Failed to mask record {i + 1}: {e}")
            errors += 1
            continue
    
    logger.info(f"Successfully masked {len(masked_data)} records")
    if errors > 0:
        logger.warning(f"{errors} records failed to mask and were skipped")
    
    return masked_data


def main(
    input_file: str = 'data/demographics.csv',
    output_file: str = 'demographicsMasked.csv',
    date_shift_days: int = 10
) -> None:
    """
    Main function to mask demographic data.
    
    Args:
        input_file: Input CSV filename (default: 'data/demographics.csv').
        output_file: Output CSV filename (default: 'demographicsMasked.csv').
        date_shift_days: Number of days to shift birth dates (default: 10).
        
    Raises:
        Exception: If masking or file operations fail.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Starting demographic data masking...")
        logger.info(f"Input file: {input_file}")
        logger.info(f"Output file: {output_file}")
        logger.info(f"Date shift: {date_shift_days} days")
        
        # Load original data
        original_data = load_demographics_data(input_file)
        
        # Mask the data
        masked_data = mask_demographics_batch(original_data, date_shift_days)
        
        # Save masked data
        save_masked_data(masked_data, output_file)
        
        # Calculate and log execution time
        end_time = time.time()
        elapsed = end_time - start_time
        
        logger.info(f"Masking completed successfully!")
        logger.info(f"Execution time: {elapsed:.2f} seconds")
        if masked_data:
            logger.info(f"Records per second: {len(masked_data)/elapsed:.2f}")
        
    except Exception as e:
        logger.error(f"Masking failed: {e}")
        raise


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Mask sensitive data in demographic datasets while preserving key characteristics.'
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        default='data/demographics.csv',
        help='Input CSV filename (default: data/demographics.csv)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='demographicsMasked.csv',
        help='Output CSV filename (default: demographicsMasked.csv)'
    )
    
    parser.add_argument(
        '-d', '--date-shift',
        type=int,
        default=10,
        help='Number of days to shift birth dates (default: 10)'
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
        if args.date_shift < 0:
            logger.error("Date shift must be non-negative")
            sys.exit(1)
            
        # Run main function
        main(args.input, args.output, args.date_shift)
        
    except KeyboardInterrupt:
        logger.info("Masking interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

