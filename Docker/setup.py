from setuptools import setup, find_packages

setup(
    name="abstract",
    version="1.0",
    packages=find_packages(),
    install_requires=[

        "requests==2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'personal_assistant=abstract:run_assistant',
        ],
    },
    author="Viktoriia",
    author_email="vikki.mrrr@gmail.com",
    description="Персональний бот-помічник в віртуальному середовищі",
)
