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
        license="GPLv3",
        description="A virtual host scanner that performs reverse lookups, "
                    "can be used with pivot tools, detect catch-all"
                    "scenarios, aliases and dynamic default pages.",
        long_description=file.read(),
        author="Luis",
        version=__version__,
        author_email="atakurban@gmail.com",
        url="https://github.com/Dzhan85/vscan",
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
