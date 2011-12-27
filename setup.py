from setuptools import setup, find_packages

setup(
    name = "amitu-dutils",
    description = "Django Utilities",
    version = "0.1.0",
    author = 'Amit Upadhyay',
    author_email = "upadhyay@gmail.com",

    url = 'http://github.com/amitu/amitu-dutils/',
    license = 'BSD',

    namespace_packages = ["amitu"],
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'amitu.serve = amitu.serve:main',
        ]
    },
)
