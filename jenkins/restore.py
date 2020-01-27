import tarfile

import boto3


def local_tarfile(archive_name, archive_path, jenkins_home):
	my_tar = tarfile.open(f'{archive_path}/{archive_name}')
	my_tar.extractall(jenkins_home)
	my_tar.close()


def remote_tarfile(bucket_name, archive_name, dest_path, jenkins_home):
	s3_resource = boto3.resource('s3')
	s3_resource.Object(bucket_name, archive_name).download_file(f'{dest_path}')
	my_tar = tarfile.open(f'{dest_path}/{archive_name}')
	my_tar.extractall(jenkins_home)
	my_tar.close()
