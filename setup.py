from setuptools import setup, find_packages
import toml

from src.ado2hugo import __version__


def get_long_description():
    with open("README.md") as file:
        return file.read()


def get_install_requires():
    data = toml.load("Pipfile")
    return [package + (version if version != "*" else "")
            for package, version in data["packages"].items()]


long_description = get_long_description()
packages = find_packages(where="src")
install_requires = get_install_requires()

setup(
    name="ado2hugo",
    version=__version__,
    author="panicoenlaxbox",
    author_email="panicoenlaxbox@gmail.com",
    description="Azure DevOps Wiki to Hugo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=packages,
    package_dir={"": "src"},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'ado2hugo = ado2hugo.__main__:main',
        ],
    },
)
