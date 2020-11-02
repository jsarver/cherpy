from distutils.core import setup
from setuptools import find_packages

setup(
    name='cherpy',
    version='0.5',
    packages=find_packages(),
    url='',
    license='',
    author='JSARVER',
    author_email='',
    description='',
    install_requires=["""attrs
                        chardet
                        click
                        idna
                        python-dateutil
                        pytz
                        PyYAML
                        requests
                        six
                        urllib3
                        loguru
                        """
                      ],
    entry_points="""
    [console_scripts]
    serviceinfo=cherpy.api:service_info
    update_object=cherpy.scripts.update_from_file:update_object_from_file_cli
    
    """,
)
