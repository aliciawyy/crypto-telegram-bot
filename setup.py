from setuptools import find_packages
from setuptools import setup

with open("requirements.txt", "r") as f:
    install_requires = [line.strip() for line in f.readlines()]

long_description = (
    "A bot to trade crypto on telegram"
)


setup(
    name="pymerkletree",
    version='0.0.1',
    description="A bot to trade crypto on telegram",
    long_description=long_description,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
    ],
    url='https://github.com/aliciawyy/crypto-telegram-bot',
    author='Alice Wang',
    author_email="rainingilove@gmail.com",
    keywords='bot, blockchain, trading, telegram',
    license="LGPLv3",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        "test": [
            "pytest==3.6.1",
            "pytest-cov==2.5.1",
        ]
    }
)
