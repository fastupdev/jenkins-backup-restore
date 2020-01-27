from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'Sample Package made for a demo \
of its making for the GeeksforGeeks Article.'

setup(
	name='jenkins',
	version='1.0',
	author='Surya Lolla',
	author_email='suryasaicharan93@gmail.com',
	description='Jenkins backup and restore cli tool.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	license='MIT',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'backup = jenkins.backup:main'
		]
	},
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
	keywords='Jenkins backup and restore',
	install_requires=requirements,
	zip_safe=False
)
