from setuptools import setup, find_packages


setup(
    name='orator',
    version='0.0.2',
    description='Audiobook generation',
    url='',
    author='Max Margenot, Kevin Ryan',
    author_email='',
    packages=find_packages(exclude=['docs', 'tests']),
    python_requires='>=3.8.0',
    install_requires=['pytest'],
    entry_points={
        'console_scripts': ['orator = orator.cli:cli']
    }
)