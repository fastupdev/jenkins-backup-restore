from setuptools import setup, find_packages
from os import path

with open('requirements.txt') as f:
	requirements = f.readlines()

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='jenkins-backup-restore-cli',
	version='1.0.2',
	author='Surya Lolla',
	author_email='suryasaicharan93@gmail.com',
	description='A Jenkins backup and restore python cli tool with arguments.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/venkatalolla/jenkins-backup-restore.git',
	license='MIT',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'jenkins-backup-restore_cli = main.jenkins_backup_restore_cli:main'
		]
	},
	classifiers=(
		"Development Status :: 3 - Alpha",
		"Intended Audience :: End Users/Desktop",
		"Intended Audience :: Developers",
		"Intended Audience :: System Administrators",
		"Topic :: System :: Systems Administration",
		"Topic :: System :: Recovery Tools",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: POSIX",
	),
	keywords='Jenkins backup and restore cli',
	install_requires=requirements,
	zip_safe=False
)
