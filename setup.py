""" __Doc__ File handle class """
from setuptools import find_packages, setup
from vscan.lib.core.__version__ import __version__


def dependencies(imported_file):
    """ __Doc__ Handles dependencies """
    with open(imported_file) as file:
        return file.read().splitlines()


with open("README.md") as file:
    num_installed = False
    try:
        import numpy
        num_installed = True
    except ImportError:
        pass
    setup(
        name="vscan",
        long_description=file.read(),
        version=__version__,
        packages=find_packages(exclude=('tests')),
        package_data={'vscan': ['*.txt']},
        entry_points={
            'console_scripts': [
                'vscan = vscan.vscan:main'
            ]
        },
        install_requires=dependencies('requirements.txt'),
        setup_requires=['pytest-runner',
                        '' if num_installed else 'numpy==1.12.0'],
        tests_require=dependencies('test-requirements.txt'),
        include_package_data=True)
