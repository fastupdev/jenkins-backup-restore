"""backup.py with make_tarfile, local_tarfile_copy, remote_tarfile_copy takes backup jenkins_home"""
import os
import shutil
import tarfile

import boto3


def make_tarfile(archive_name, jenkins_home):
    """make_tarfile(archive_name, jenkins_home) will tar the jenkins_home directory"""
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(jenkins_home, arcname=os.path.basename(jenkins_home))


def local_tarfile_copy(archive_name, dest_location):
    """local_tarfile_copy is to move a tar from one location to another location"""
    shutil.move(archive_name, dest_location)


def remote_tarfile_copy(bucket_name, archive_name):
    """remote_tarfile_copy move the tar file from a local dir to an s3 bucket. For this
    method to work, the AWS credentials should be preset in the terminal from where ever you are
    running the jenkins-backup-restore-cli from."""
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket_name, archive_name).upload_file(Filename=archive_name)
    os.remove(archive_name)
