from setuptools import setup

setup(
    name='ReportGenerator',
    version='0.1',
    description='Report generate module',
    url='https://github.com/whatever/whatever',
    author='AIST',
    author_email='your@address.com',
    keywords='report',
    packages=[
        "reportgenerator"
    ],
    install_requires=[
        "pandas==1.2.0",
        "pdfkit==0.6.1"
    ]
)