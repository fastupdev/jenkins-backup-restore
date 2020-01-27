from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'Jenkins backup and restore packages \
with access to push and pull from a local directory or an s3 bucket.'

setup(
	name='jenkins-bkp-rst',
	version='1.0',
	author='Surya Lolla',
	author_email='suryasaicharan93@gmail.com',
	description='Jenkins backup and restore cli tool.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	license='MIT',
	packages=find_packages(),
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
	keywords='Jenkins backup and restore',
	install_requires=requirements,
	zip_safe=False
)
