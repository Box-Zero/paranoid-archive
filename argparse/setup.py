from setuptools import setup

setup(
    name='paranoid-archive',
    version=1.0,
    packages=['paranoid-archive'],
    install_requires=['pytest'],
    entry_points={'console_scripts': ['paranoid-archive = paranoid-archive.cli.main:main']}
)
