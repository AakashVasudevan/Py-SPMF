"""spmf - setup.py"""
from setuptools import find_packages, setup

LONG_DESC = open('README.md').read()

setup(
    name='spmf-wrapper',
    version='{{VERSION_PLACEHOLDER}}',
    author='Aakash Vasudevan',
    author_email='Aakash.Vasudevan@gmail.com',
    description='Python Wrapper for SPMF',
    long_description_content_type='text/markdown',
    long_description=LONG_DESC,
    url='https://github.com/AakashVasudevan/Py-SPMF',
    include_package_data=True,
    packages=find_packages() + ['spmf/binaries'],
    install_requires=['pandas>=1.4.3', 'install-jdk<=1.1.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    keywords=['SPMF', 'pattern', 'mining']
)
