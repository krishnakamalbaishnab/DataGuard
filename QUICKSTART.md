# DataGuard Quick Start Guide 🚀

This guide shows you how to set up and run the DataGuard project step by step.

## 📋 Prerequisites

- **Python 3.7+** (check with `python --version` or `python3 --version`)
- **pip** package manager

## 🛠️ Installation

### Option 1: Install Dependencies (Recommended)
```bash
# Install required packages
pip install -r requirements.txt

# Alternative if you use pip3
pip3 install -r requirements.txt
```

### Option 2: Manual Installation
```bash
pip install faker>=20.0.0 python-dateutil>=2.8.0
```

## 🎯 Running the Project

### 1. **Test the Installation**
First, verify everything works:

```bash
# Run basic functionality tests
python test_basic.py

# See comprehensive examples
python example_usage.py

# Check configuration
python config.py
```

### 2. **Generate Synthetic Data**

#### Basic Usage:
```bash
# Generate 100 synthetic demographic records (default)
python DemographicsGenerator.py
```

#### Advanced Usage:
```bash
# Generate 500 records with verbose output
python DemographicsGenerator.py -n 500 -v

# Generate 1000 records to custom file
python DemographicsGenerator.py -n 1000 -o my_synthetic_data.csv

# See all options
python DemographicsGenerator.py --help
```

#### Output:
- Creates `demographicsData.csv` (or your custom filename)
- Contains: SSN, credit card, name, address, email, phone

### 3. **Mask Existing Data**

#### Basic Usage:
```bash
# Mask the sample data (uses data/demographics.csv)
python DemographicsMasking.py
```

#### Advanced Usage:
```bash
# Mask custom input file with 20-day date shift
python DemographicsMasking.py -i my_data.csv -o masked_output.csv -d 20

# Verbose masking with custom parameters
python DemographicsMasking.py -i data/demographics.csv -o secured_data.csv -d 15 -v

# See all options
python DemographicsMasking.py --help
```

#### Output:
- Creates `demographicsMasked.csv` (or your custom filename)
- Preserves gender but replaces all other PII with fake data

## 📁 Understanding the Files

### Input Files:
- `data/demographics.csv` - Sample input data for masking

### Output Files:
- `demographicsData.csv` - Generated synthetic data
- `demographicsMasked.csv` - Masked version of input data

### Project Files:
- `DataMasker.py` - Core functions for generating fake data
- `DemographicsGenerator.py` - Script to generate synthetic datasets
- `DemographicsMasking.py` - Script to mask existing data
- `config.py` - Configuration settings
- `example_usage.py` - Examples and demonstrations
- `test_basic.py` - Basic functionality tests

## 💻 Programming Usage

### Import and Use in Your Code:
```python
import DataMasker

# Generate individual components
name = DataMasker.generateName('Female')
print(f"Name: {name['firstName']} {name['lastName']}")

address = DataMasker.generateAddress()
print(f"Address: {address['address']}")

contact = DataMasker.generateContact()
print(f"Email: {contact['email']}")

# Generate complete record
record = DataMasker.generateDemographics()
```

### Use the Improved Modules:
```python
from DemographicsGenerator import generate_batch, save_to_csv
from DemographicsMasking import mask_demographic_record

# Generate 50 records
records = generate_batch(50)
save_to_csv(records, "my_data.csv")

# Mask a single record
original = {'birthDate': '01-01-1990', 'gender': 'Male'}
masked = mask_demographic_record(original, date_shift_days=15)
```

## 🔧 Configuration

### Environment Variables:
```bash
# Set custom defaults
export DATAGUARD_RECORD_COUNT=1000
export DATAGUARD_DATE_SHIFT_DAYS=20
export DATAGUARD_FAKER_LOCALE=en_GB

# Run with custom settings
python DemographicsGenerator.py
```

### Edit config.py:
Modify `config.py` to change default behaviors:
- Record counts
- Date shift amounts
- File paths
- Logging levels

## 🚨 Common Issues & Solutions

### Issue 1: "Module not found" errors
**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install faker python-dateutil
```

### Issue 2: "No such file" for input data
**Solution:**
```bash
# Check if data directory exists
ls data/

# Use absolute path
python DemographicsMasking.py -i /full/path/to/your/data.csv
```

### Issue 3: Permission errors on output files
**Solution:**
```bash
# Make sure output directory is writable
# Or specify different output location
python DemographicsGenerator.py -o ~/Desktop/output.csv
```

## 📊 Example Workflows

### Workflow 1: Quick Data Generation
```bash
# Generate test data for development
python DemographicsGenerator.py -n 100 -o test_data.csv -v
```

### Workflow 2: Production Data Masking
```bash
# Mask production data for testing
python DemographicsMasking.py \
  -i production_data.csv \
  -o masked_for_testing.csv \
  -d 30 \
  -v
```

### Workflow 3: Batch Processing
```bash
# Generate multiple datasets
for i in {1..5}; do
  python DemographicsGenerator.py -n 200 -o "dataset_$i.csv"
done
```

## 🔍 Verification

### Check Your Output:
```bash
# View first few lines of generated data
head -5 demographicsData.csv

# Count records
wc -l demographicsData.csv

# View specific columns
cut -d',' -f1,3,4 demographicsData.csv | head -5
```

## 🎓 Next Steps

1. **Customize for Your Needs**: Edit `config.py` for your requirements
2. **Integrate with Your Pipeline**: Import modules into your existing code
3. **Scale Up**: Use command-line tools for batch processing
4. **Extend Functionality**: Add new data types by modifying `DataMasker.py`

## 🆘 Getting Help

- Run any script with `--help` flag for detailed options
- Check `example_usage.py` for code examples
- Run `test_basic.py` to verify functionality
- Review the main `README.md` for comprehensive documentation

---

**Ready to protect your data? Start with:**
```bash
python test_basic.py && python example_usage.py
``` 