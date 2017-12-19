from setuptools import setup

setup(
    name='LoLsearch',
    version='0.1.0',
    package=['app'],
    include_package_data=True,
    install_requires=[
        'requests',
        'discord',
        'pycodestyle',
        'pydocstyle',
        'pylint'
    ],
)