from setuptools import setup, find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name='qlib',
    license='Apache License 2.0',
    description='AIT Software Development Kit',
    url='https://github.com/aistairc/qai-testbed',
    author='AIST',
    author_email='your@address.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    keywords=['QAI', 'AIT'],
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"]
)
