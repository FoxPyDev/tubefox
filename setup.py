from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tubefox',
    version='0.8.7',
    author='@FoxPyDev Yaroslav Lysenko',
    author_email='foxpythondev@gmail.com',
    description="A package for scraping YouTube data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FoxPyDev/tubefox",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'requests',
        'lxml'
    ],
)