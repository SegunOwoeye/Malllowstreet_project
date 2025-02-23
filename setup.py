from setuptools import setup, find_packages

setup(
    name="Mallowstreet_Project",  # Replace with your project name
    version="1.0",
    packages=find_packages(),  # Automatically find all subpackages
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pdfplumber",
        "pandas",
        "openpyxl"
    ],  # Add any dependencies here 
)
