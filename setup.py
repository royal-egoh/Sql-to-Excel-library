from setuptools import setup, find_packages

setup(
    name="exlsql",
    version="0.1.3",
    packages=find_packages(),
    install_requires=["pandas"],
    author="royal-egoh",
    description="SQL-like queries for Excel files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)