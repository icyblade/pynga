from setuptools import setup

about = {}
with open('./pynga/__version__.py', 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

tests_require = [
    'pytest>=3.5.0,<3.7.0',
    'pytest-flake8>=1.0.0'
]

setup(
    name=about['__title__'],
    version=about['__version__'],
    packages=['pynga'],
    url=about['__url__'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'requests>=2.10.0',
        'cachecontrol>=0.12.0',
        'beautifulsoup4>=4.0.0',
        'urllib3>=1.18',
        'pytz>=2017.2',
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    python_requires='>=3.6',
)
