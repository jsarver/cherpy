from distutils.core import setup
from setuptools import find_packages

setup(
    name='cherpy',
    version='0.0.3',
    packages=find_packages(),
    url='',
    license='',
    author='JSARVER',
    author_email='',
    description='',
    install_requires=["""attrs==17.2.0
                        certifi==2017.7.27.1
                        chardet==3.0.4
                        click==6.7
                        idna==2.5
                        python-dateutil==2.6.1
                        pytz==2017.2
                        PyYAML==4.2b1
                        requests==2.20.0
                        six==1.10.0
                        urllib3==1.23"""
                      ],
    entry_points="""
    [console_scripts]
    query_object=cherpy.scripts.query_object:cli
    delete_objects=cherpy.scripts.delete_object:delete_cli
    update_object=cherpy.scripts.update_from_file:update_object_from_file_cli
    
    """,
)
