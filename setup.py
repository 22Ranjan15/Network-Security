"""
    The setup.py file essential part of packaging and distributing Python projects.
    It is uesed by setup tools (or distributils in older python versions) to define the
    configuration of our project, such as its metadata, dependencies, and more
"""

from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    # This function will return list of requirements
    requirement_list:List[str]=[]
    try:
        with open('requirements.txt', 'r') as file:
            # read lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                # Remove all spaces before and after the line
                requirement = line.strip()
                # Ignore empty lines and -e.
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_list

setup(
    name = "Network Security",
    version="0.0.1",
    author="Ranjan",
    author_email="ranjandasbd22@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)