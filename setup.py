from __future__ import unicode_literals

from setuptools import setup, find_packages

setup(
    name='passreset',
    version='0.3',
    author='Ben Davis',
    author_email='bendavis78@gmail.com',
    url='http://github.com/bendavis78',
    description='Easily add password reset workflows to your django project.',
    keywords='django admin',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    include_package_data=True
)
