import os
from setuptools import setup, find_packages

def get_requirements():
    if os.path.exists('requirements.txt'):
        with open('requirements.txt') as f:
            requirements = f.read().splitlines()
        return requirements
    return []

setup(
    name='END TO END RECIPE RECOMMENDER SYSTEM',
    version='0.1',
    author='Your Name',
    description='Description of your project',
    packages=find_packages(),
    install_requires=get_requirements()

)


