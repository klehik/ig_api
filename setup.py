import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='ig_api',  
    version='0.0.1',
    author="Kalle Lehikoinen",
    author_email="kalle.lehikoinen@gmail.com",
    description="Simple library to make requests to IG graph api",
    install_requires=['python-dotenv', 'requests'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lol.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )