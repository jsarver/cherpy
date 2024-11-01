from setuptools import setup
from setuptools import find_packages

setup(
    name='cherpy',
    version='0.5.2',
    packages=find_packages(),
    url='',
    license='',
    author='Josh Sarver',
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
    entry_points="""
        [console_scripts]
        search=cherpy.cli:search_object_cli
        delete_objects=cherpy.cli:delete_objects_cli
        update=cherpy.cli:update_object_cli
        create=cherpy.cli:create_object
        run-onestep=cherpy.cli:run_onestep_cli
        csm=cherpy.cli:csm
        """

)
