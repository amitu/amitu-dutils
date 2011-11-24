from setuptools import setup

setup(
    name = "amitu-zutils",
    version = "0.1.1",
    url = 'http://packages.python.org/amitu-zutils/',
    license = 'BSD',
    description = "Generic Utilities for ZMQ based services",
    author = 'Amit Upadhyay',
    author_email = "upadhyay@gmail.com",
    py_modules = [
        "amitu.zutils", "amitu.zidgen", "amitu.zconfig", "amitu.zqueue"
    ],
    namespace_packages = ["amitu"],
)
