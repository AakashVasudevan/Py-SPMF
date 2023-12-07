"""spmf - setup.py"""
import setuptools

LONG_DESC = open('README.md').read()

setuptools.setup(
    name='spmf',
    version='0.0.1',
    author='Aakash Vasudevan',
    author_email='Aakash.Vasudevan@gmail.com',
    description='Python Wrapper for SPMF',
    long_description_content_type='text/markdown',
    long_description=LONG_DESC,
    url='https://github.com/AakashVasudevan/Py-SPMF',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
)
