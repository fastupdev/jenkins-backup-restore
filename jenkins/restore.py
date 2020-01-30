"""restore.py with below local_tarfile and remote_tarfile methods restores the jenkins backup"""
import tarfile
import os
import shutil
import boto3
import botocore


def local_tarfile(archive_name, archive_path, jenkins_home):
    """local_tarfile extracts a tar file in a user specified location"""
    my_tar = tarfile.open(f'{archive_path}/{archive_name}')
    my_tar.extractall(jenkins_home)
    my_tar.close()


def remote_tarfile(bucket_name, archive_name, dest_path, jenkins_home):
    """remote_tarfile not only pulls the tar from the s3 bucket but also extracts the
    tar file in the user specified location, For this method to work, the AWS credentials
    should be preset in the terminal from where ever you are running the
    jenkins-backup-restore-cli from."""
    s3_resource = boto3.client('s3')
    try:
        s3_resource.download_file(bucket_name, archive_name, f'{dest_path}/{archive_name}')
    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    extract_dir = jenkins_home.replace('jenkins_home', '')
    shutil.unpack_archive(f'{dest_path}/{archive_name}', extract_dir)
    os.remove(f'{dest_path}/{archive_name}')
