import os.path
import pathlib
from os.path import exists
from setuptools import setup, find_packages


CURRENT_DIR = pathlib.Path(__file__).parent
long_description = ""
readme_md_file = os.path.join(CURRENT_DIR, "README.md")
if exists(readme_md_file):
    long_description = pathlib.Path(readme_md_file).read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = ["qrcode", "weasyprint==52.5"]

    if env and env == "dev":
        return dependency

    return dependency + []


setup(
    name='rpi-portal',
    version='0.0.1',
    url='#',
    license='Problem Fighter License',
    author='Problem Fighter',
    author_email='proma@problemfighter.com',
    description='',
    long_description=long_description,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    classifiers=[]
)
