from setuptools import setup
from setuptools import find_packages

setup(
    name='cherpy',
    version='0.5.2',
    packages=find_packages(),
    url='',
    license='',
    author='Josh sarver',
    author_email='josh.sarver@gmail.com',
    description='A rest api wrapper for the Cherwell Service management platform',
    install_requires=["""attrs
                        chardet
                        PyYAML
                        requests == 2.32.0
                        loguru
                        """
                      ],
    python_requires='>=3.9',
)
