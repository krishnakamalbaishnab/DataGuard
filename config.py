"""
DataGuard Configuration Settings.

This module contains configurable parameters for data masking and generation.
Modify these settings to customize the behavior of DataGuard tools.
"""

import os
from pathlib import Path
from typing import Dict, List, Union

# =============================================================================
# File Paths and Directories
# =============================================================================

# Default input directory for data files
DEFAULT_INPUT_DIR = Path("data")

# Default output directory for generated/masked files
DEFAULT_OUTPUT_DIR = Path(".")

# Default input file for masking operations
DEFAULT_INPUT_FILE = DEFAULT_INPUT_DIR / "demographics.csv"

# Default output files
DEFAULT_MASKED_OUTPUT = DEFAULT_OUTPUT_DIR / "demographicsMasked.csv"
DEFAULT_GENERATED_OUTPUT = DEFAULT_OUTPUT_DIR / "demographicsData.csv"

# =============================================================================
# Data Generation Settings
# =============================================================================

# Default number of records to generate
DEFAULT_RECORD_COUNT = 100

# Default locale for Faker (affects names, addresses, phone formats, etc.)
FAKER_LOCALE = 'en_US'  # Options: 'en_US', 'en_GB', 'de_DE', 'fr_FR', etc.

# =============================================================================
# Data Masking Settings
# =============================================================================

# Default number of days to shift birth dates
DEFAULT_DATE_SHIFT_DAYS = 10

# Whether to preserve original data relationships
PRESERVE_RELATIONSHIPS = True

# Date format for output files
OUTPUT_DATE_FORMAT = '%m-%d-%Y'

# =============================================================================
# CSV Field Definitions
# =============================================================================

# Standard field names for generated demographic data
GENERATED_FIELDS = [
    'ssn',
    'creditCard', 
    'firstName',
    'lastName',
    'address',
    'city',
    'state',
    'postalCode',
    'email',
    'phone'
]

# Standard field names for masked demographic data
MASKED_FIELDS = [
    'ssn',
    'birthDate',
    'gender',
    'firstName',
    'lastName',
    'address',
    'city',
    'state',
    'postalCode',
    'email',
    'phone'
]

# =============================================================================
# Logging Configuration
# =============================================================================

# Default logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = 'INFO'

# Log format string
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Whether to log to file in addition to console
LOG_TO_FILE = False

# Log file path (only used if LOG_TO_FILE is True)
LOG_FILE_PATH = Path("logs") / "dataguard.log"

# =============================================================================
# Data Validation Settings
# =============================================================================

# Required fields for input data validation
REQUIRED_INPUT_FIELDS = ['birthDate', 'gender']

# Maximum number of errors to tolerate during batch processing
MAX_ERROR_THRESHOLD = 0.1  # 10% of records

# Whether to skip invalid records or halt processing
SKIP_INVALID_RECORDS = True

# =============================================================================
# Performance Settings
# =============================================================================

# Batch size for progress reporting
PROGRESS_BATCH_SIZE = 100

# Maximum number of records to process in memory at once
MAX_MEMORY_RECORDS = 10000

# =============================================================================
# Security and Privacy Settings
# =============================================================================

# Whether to generate deterministic fake data (same seed = same output)
DETERMINISTIC_OUTPUT = False

# Random seed for deterministic output (only used if DETERMINISTIC_OUTPUT is True)
RANDOM_SEED = 42

# Fields that should never appear in logs for security
SENSITIVE_FIELDS = ['ssn', 'creditCard', 'email']

# =============================================================================
# Advanced Masking Options
# =============================================================================

# Custom date shift ranges (min_days, max_days) for more randomized shifting
DATE_SHIFT_RANGE = None  # Set to tuple like (-30, 30) for random shifts

# Gender preservation during name generation
PRESERVE_GENDER = True

# Address localization (ensure generated addresses match original locale)
LOCALIZE_ADDRESSES = True

# =============================================================================
# Utility Functions
# =============================================================================

def get_config_value(key: str, default: Union[str, int, bool, None] = None) -> Union[str, int, bool, None]:
    """
    Get a configuration value, checking environment variables first.
    
    Args:
        key: Configuration key name.
        default: Default value if not found.
        
    Returns:
        Configuration value from environment or default.
    """
    env_key = f"DATAGUARD_{key.upper()}"
    return os.environ.get(env_key, default)


def validate_config() -> Dict[str, str]:
    """
    Validate configuration settings and return any issues found.
    
    Returns:
        Dict containing validation warnings/errors.
    """
    issues = {}
    
    # Check if input directory exists
    if not DEFAULT_INPUT_DIR.exists():
        issues['input_dir'] = f"Input directory {DEFAULT_INPUT_DIR} does not exist"
    
    # Check if required fields are defined
    if not REQUIRED_INPUT_FIELDS:
        issues['required_fields'] = "No required input fields defined"
    
    # Validate date shift settings
    if DEFAULT_DATE_SHIFT_DAYS < 0:
        issues['date_shift'] = "Date shift days should be non-negative"
    
    # Validate error threshold
    if not (0 <= MAX_ERROR_THRESHOLD <= 1):
        issues['error_threshold'] = "Error threshold must be between 0 and 1"
    
    return issues


def get_effective_config() -> Dict[str, Union[str, int, bool, Path]]:
    """
    Get the effective configuration with environment variable overrides.
    
    Returns:
        Dictionary of effective configuration values.
    """
    return {
        'input_dir': Path(get_config_value('input_dir', DEFAULT_INPUT_DIR)),
        'output_dir': Path(get_config_value('output_dir', DEFAULT_OUTPUT_DIR)),
        'record_count': int(get_config_value('record_count', DEFAULT_RECORD_COUNT)),
        'date_shift_days': int(get_config_value('date_shift_days', DEFAULT_DATE_SHIFT_DAYS)),
        'faker_locale': get_config_value('faker_locale', FAKER_LOCALE),
        'log_level': get_config_value('log_level', LOG_LEVEL),
        'preserve_gender': bool(get_config_value('preserve_gender', PRESERVE_GENDER)),
        'deterministic': bool(get_config_value('deterministic_output', DETERMINISTIC_OUTPUT)),
    }


if __name__ == "__main__":
    # Print current configuration for debugging
    print("DataGuard Configuration")
    print("=" * 50)
    
    config = get_effective_config()
    for key, value in config.items():
        print(f"{key}: {value}")
    
    print("\nValidation Issues:")
    issues = validate_config()
    if issues:
        for key, issue in issues.items():
            print(f"  {key}: {issue}")
    else:
        print("  No issues found") 