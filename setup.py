from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name= "Hotel_Reservation_Project",
    version= "0.1",
    author= "Yajat",
    packages= find_packages(),
    install_requires= requirements
)    

# executed this file using the following command: pip install -e . 