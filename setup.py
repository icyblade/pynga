from setuptools import setup

from .pynga.__version__ import (__title__, __description__, __url__, __version__,
                                __license__, __author__, __author_email__)

setup(
    name=__title__,
    version=__version__,
    packages=['pynga'],
    url=__url__,
    license=__license__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
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
