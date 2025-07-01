# DataGuard 🛡️

A Python toolkit for data masking and synthetic data generation to help organizations comply with privacy regulations like GDPR, CCPA, and HIPAA.

## 🚀 Features

- **Data Masking**: Transform sensitive production data while preserving data relationships and characteristics
- **Synthetic Data Generation**: Create realistic fake datasets for testing and development
- **Privacy Compliance**: Help maintain data utility while protecting personally identifiable information (PII)
- **Flexible Configuration**: Customizable masking strategies for different data types

## 📁 Project Structure

```
DataGuard/
├── DataMasker.py           # Core masking utilities and fake data generators
├── DemographicsGenerator.py # Generate synthetic demographic datasets
├── DemographicsMasking.py  # Mask existing demographic data
├── data/
│   └── demographics.csv    # Sample input data
├── requirements.txt        # Python dependencies
├── LICENSE                # MIT License
└── README.md              # This file
```

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd DataGuard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Data Masking

Mask sensitive data from existing datasets while preserving key characteristics:

```bash
python DemographicsMasking.py
```

This will:
- Read data from `data/demographics.csv`
- Generate fake names based on original gender
- Shift birth dates by 10 days to maintain age relationships
- Replace all PII with realistic fake data
- Output masked data to `demographicsMasked.csv`

### Synthetic Data Generation

Generate completely synthetic demographic data:

```bash
python DemographicsGenerator.py
```

This will:
- Generate 100 synthetic demographic records
- Create realistic names, addresses, phone numbers, and emails
- Output data to `demographicsData.csv`

### Custom Usage

```python
import DataMasker

# Generate fake identity
name = DataMasker.generateName(gender='Female')
address = DataMasker.generateAddress()
contact = DataMasker.generateContact()

print(f"Name: {name['firstName']} {name['lastName']}")
print(f"Address: {address['address']}, {address['city']}, {address['state']}")
print(f"Email: {contact['email']}")
```

## 🔧 Available Functions

### DataMasker.py

| Function | Description | Parameters |
|----------|-------------|------------|
| `generateName(gender)` | Generate fake names | `gender`: 'Male', 'Female', or None |
| `generateAddress()` | Generate fake addresses | None |
| `generateContact()` | Generate email and phone | None |
| `generateSSN()` | Generate fake SSN | None |
| `generateCreditCardNumber()` | Generate fake credit card | None |
| `generate_uuid()` | Generate UUID | None |
| `add_days(date, days)` | Add days to a date | `date`: datetime, `days`: int |

## 📊 Data Types Supported

- **Personal Information**: Names, SSNs, emails, phone numbers
- **Financial Data**: Credit card numbers
- **Geographic Data**: Addresses, cities, states, postal codes
- **Temporal Data**: Birth dates with configurable shifts
- **Identifiers**: UUIDs

## 🔒 Privacy & Security

- **No Real Data Storage**: Sample data should be replaced with your own test data
- **Configurable Masking**: Adjust date shifts and other parameters as needed
- **Compliance Ready**: Designed to help with GDPR, CCPA, and HIPAA requirements

## 🐛 Known Issues & Improvements

See the [Issues & Improvements](#issues--improvements) section below for planned enhancements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For questions or support, please open an issue on the GitHub repository.

---

## 🔍 Issues & Improvements

### Identified Issues:
1. **Hard-coded values** (10-day date shift, file paths)
2. **Missing error handling** for file operations
3. **No input validation**
4. **Limited configurability**
5. **No logging capabilities**

### Suggested Improvements:
1. **Add configuration file** for customizable parameters
2. **Implement proper error handling** and logging
3. **Add type hints** for better code documentation
4. **Create unit tests** for reliability
5. **Add CLI interface** with argument parsing
6. **Support for multiple file formats** (JSON, Parquet, etc.)
7. **Batch processing** for large datasets
8. **Custom masking strategies** per field type
9. **Data quality validation** before and after masking
10. **Docker containerization** for easy deployment