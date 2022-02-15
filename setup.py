# setup.py
import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="mrf_parser",
    version="0.0.1",
    author="Paul Zuradzki",
    author_email="paulzuradzki@gmail.com",
    license="MIT",
    description="This is a package for parsing provider machine readable files which are required pursuant to CMS Price Transparency regulations.",
    long_description=README,
    long_description_content_type="text/markdown",    
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=['beautifulsoup4', 'pandas>=1.3.0', 'requests', 'lxml', 'openpyxl', 'tabulate'],
)