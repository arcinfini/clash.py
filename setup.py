import setuptools

VERSION = '0.1.0'

REQUIREMENTS = []
with open('requirements.txt', 'r') as file:
    REQUIREMENTS = file.readlines()

README = ""
with open("README.md", "r", encoding="utf-8") as file:
    README = file.read()

setuptools.setup(
    name="clash.py", # Replace with your own username
    version=VERSION,
    author="arcinfini",
    description="A base implementation of the Clash of Clans API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arcinfini/clash.py",
    packages=['clash'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)