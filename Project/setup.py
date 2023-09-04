from setuptools import setup, find_packages

setup(
    name='Project',
    version='1.0',
    description='Page of web app',
    author='Viktoriia',
    author_email='vikki.mrrr@gmail.com',
    url='https://github.com/Vikka777/Tutorial',
    packages=find_packages(),
    install_requires=[
        'pipenv==2023.9.1',
        'requests==2.31.0',
        'certifi>=2017.4.17',
        'charset-normalizer>=2,<4',
        'idna>=2.5,<4',
        'urllib3>=1.21.1,<3',
    ],
)
