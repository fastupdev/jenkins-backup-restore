import io
import os
from os import path

from setuptools import setup, find_packages


def read(reqpath, encoding='utf-8'):
    reqpath = os.path.join(os.path.dirname(__file__), reqpath)
    with io.open(reqpath, encoding=encoding) as fp:
        return fp.read()


def get_install_requirements(reqpath):
    content = read(reqpath)
    return [
        req
        for req in content.split("\n")
        if req != '' and not req.startswith('#')
        ]


INSTALL_REQUIRES = get_install_requirements("requirements.txt")

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jenkins-backup-restore-cli',
    version='1.1.4',
    author='Venkata Surya Lolla',
    author_email='suryasaicharan93@gmail.com',
    description='A Jenkins backup and restore python cli tool with arguments.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Code": "https://github.com/fastupdev/jenkins-backup-restore",
        "Issue tracker": "https://github.com/fastupdev/jenkins-backup-restore/issues"
    },
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jenkins-backup-restore-cli = jenkins_backup_restore_cli.jenkins_backup_restore_cli:jenkins_backup_restore_cli'
            ]
        },
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Framework :: Click",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Recovery Tools",
        ),
    keywords='Jenkins backup and restore cli',
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    zip_safe=False
    )
