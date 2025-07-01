"""
Setup configuration for DataGuard data masking toolkit.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().strip().split('\n')

setup(
    name="dataguard",
    version="1.0.0",
    author="DataGuard Project",
    author_email="support@dataguard.example.com",
    description="A Python toolkit for data masking and synthetic data generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/DataGuard",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/DataGuard/issues",
        "Source": "https://github.com/yourusername/DataGuard",
        "Documentation": "https://github.com/yourusername/DataGuard#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords="data masking, privacy, GDPR, synthetic data, fake data, anonymization",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dataguard-generate=DemographicsGenerator:main",
            "dataguard-mask=DemographicsMasking:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["data/*.csv", "*.md", "*.txt"],
    },
    zip_safe=False,
    platforms=["any"],
) 