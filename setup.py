#! /usr/bin/env python

from setuptools import find_packages, setup

print find_packages()

setup(
    name="Statkube",
    version="0.1",
    description="Fetch pull requests stats from Github",
    author="Mirantis",
    author_email='sbrzeczkowski@mirantis.com',
    license="Apache 2.0",
    url="https://github.com/gitfred/statkube",
    package_data={'statkube': ['statkube/settings.yaml']},
    packages=find_packages(),
        entry_points={
            'console_scripts': [
                'statkube = statkube.__main__:main'
            ]
    }
)
