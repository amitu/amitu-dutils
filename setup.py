from setuptools import setup, find_packages

setup(
    name = "amitu-zutils",
    description = "Generic Utilities for ZMQ based services",
    version = "0.1.2",
    author = 'Amit Upadhyay',
    author_email = "upadhyay@gmail.com",

    url = 'http://packages.python.org/amitu-zutils/',
    license = 'BSD',

    namespace_packages = ["amitu"],
    packages = find_packages(),
)
