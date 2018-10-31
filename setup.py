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
    install_requires=['click'],
    entry_points="""
    [console_scripts]
    query_object=cherpy.scripts.query_object:cli
    delete_objects=cherpy.scripts.delete_object:delete_cli
    update_object=cherpy.scripts.update_from_file:update_object_from_file_cli
    
    """,
)
