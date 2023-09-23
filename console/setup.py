from setuptools import setup, find_packages

setup(
    name='console_utilite',
    version='1.0',
    description='Console Utilite',
    author='Viktoriia',
    author_email='vikki.mrrr@gmail.com',
    url='https://github.com/Vikka777/Tutorial/tree/console_utilite',
    packages=find_packages(),
    install_requires=[
        'aiofile==3.8.8',
        'aiohttp==3.8.5',
        'aiopath==0.6.11',
        'aiosignal==1.3.1',
        'anyio==3.7.1',
        'async-timeout==4.0.3',
        'attrs==23.1.0',
        'caio==0.9.13',
        'charset-normalizer==3.2.0',
        'frozenlist==1.4.0',
        'idna==3.4',
        'multidict==6.0.4',
        'sniffio==1.3.0',
        'yarl==1.9.2',
    ],
)
