import tarfile
import os
import boto3
import botocore
import shutil


def local_tarfile(archive_name, archive_path, jenkins_home):
	my_tar = tarfile.open(f'{archive_path}/{archive_name}')
	my_tar.extractall(jenkins_home)
	my_tar.close()


def remote_tarfile(bucket_name, archive_name, dest_path, jenkins_home):
	s3_resource = boto3.client('s3')
	try:
		s3_resource.download_file(bucket_name, archive_name, f'{dest_path}/{archive_name}')
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			print("The object does not exist.")
		else:
			raise
	extract_dir = jenkins_home.replace('jenkins_home', '')
	shutil.unpack_archive(f'{dest_path}/{archive_name}', extract_dir)
	os.remove(f'{dest_path}/{archive_name}')
