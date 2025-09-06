from setuptools import setup, find_packages

setup(
    name="mysql-schema-diff",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.26.0",
        "mysql-connector-python>=8.1.0",
        "pandas>=2.1.0",
        "jinja2>=3.1.2",
    ],
)
