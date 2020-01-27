import os
import shutil
import tarfile

import boto3


def make_tarfile(archive_name, jenkins_home):
	with tarfile.open(archive_name, "w:gz") as tar:
		tar.add(jenkins_home, arcname=os.path.basename(jenkins_home))


def local_tarfile_copy(archive_name, dest_location):
	shutil.move(archive_name, dest_location)


def remote_tarfile_copy(bucket_name, archive_name):
	s3_resource = boto3.resource('s3')
	s3_resource.Object(bucket_name, archive_name).upload_file(Filename=archive_name)
	os.remove(archive_name)
