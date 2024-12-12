from setuptools import setup, find_packages

setup(
    name='algo_tester',
    version='0.1.0',
    description='A project that includes algo_tester and argument_generator',
    author='John Zhang',
    author_email='johnzhanguoft@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=[
        'matplotlib>3.0',
        'statistics; python_version<"3.8"',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
