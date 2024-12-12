from setuptools import setup, find_packages

setup(
    name='algo_tester',
    version='0.1.0',
    description='A project that includes algo_tester and argument_generator',
    author='John Zhang',
    author_email='johnzhanguoft@gmail.com',
    packages=find_packages(where='src'),  # Finds all packages in src
    package_dir={'': 'src'},              # Tells setuptools that packages are under src
    python_requires='>=3.6',
    install_requires=[
        'matplotlib',
        'statistics; python_version<"3.8"',  # statistics is in Python 3.8+, just example
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
