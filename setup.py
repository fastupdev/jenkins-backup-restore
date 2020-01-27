from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'Jenkins backup the /var/jenkins_home directory and restore it. \
Optional flags to store in local directory and push and pull from an s3 bucket.'

setup(
	name='jenkins-backup-restore',
	version='1.0',
	author='Surya Lolla',
	author_email='suryasaicharan93@gmail.com',
	description='Jenkins backup and restore python cli tool with arguments.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/venkatalolla/jenkins-backup-restore.git',
	license='MIT',
	packages=find_packages(),
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
	),
	keywords='Jenkins backup and restore',
	install_requires=requirements,
	zip_safe=False
)
