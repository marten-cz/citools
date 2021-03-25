from setuptools import setup

setup(
    name='pagewiser-ci-cd-tools',
    description="Easy VCS-based management of project version strings",
    author="Martin Malek",
    author_email="github@marten-online.com",
    license="public domain",
    version='0.1.0',
    packages=['cctools'],
    include_package_data=True,
    install_requires=[
        'click==7.0',
        'pyyaml==5.4'
    ],
    entry_points={
        'console_scripts': {
            'cctools=cctools.cli:cli'
        }
    }
)
