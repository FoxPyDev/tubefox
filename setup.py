from setuptools import setup, find_packages

setup(
    name='tubefox',
    version='0.8.1',
    author='@FoxPyDev Yaroslav Lysenko',
    author_email='foxpythondev@gmail.com',
    description='A library for scraping metadata and downloading YouTube videos',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
        'tqdm'
    ],
)
