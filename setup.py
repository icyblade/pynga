from setuptools import setup

setup(
    name='pynga',
    version='2.0.0',
    packages=['pynga'],
    url='https://github.com/icyblade/pynga',
    license='MIT',
    author='Icyblade Dai',
    author_email='icyblade.aspx@gmail.com',
    description='Python implementation of bbs.ngacn.cc',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'requests>=2.10.0',
        'cachecontrol>=0.12.0',
        'beautifulsoup4>=4.0.0',
        'urllib3>=1.18',
        'pytz>=2017.2',
    ],
    tests_require=[
        'pytest>=3.5.0',
        'pytest-flake8>=1.0.0'
    ],
    python_requires='>=3.6',
)
