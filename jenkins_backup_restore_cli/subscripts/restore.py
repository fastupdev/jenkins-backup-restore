"""restore.py with below _make_tmp_dir_and_move_tar_to_tmp, local_tarfile_restore and remote_tarfile methods restores the jenkins backup"""
import os
import shutil
import tarfile
import time
import boto3
import botocore
import click
import errno
from pathlib import Path


def _make_tmp_dir(tmp_restore_destination_path, restore_archive_path):

    # If user given restore_archive_path exists,
    if os.path.exists(restore_archive_path):
        # Create the tmp_directory
        try:
            os.makedirs(tmp_restore_destination_path)
        except OSError:
            print("Creation of the directory %s failed" % tmp_restore_destination_path)


def _untar_archive_replace_jenkins_home(tmp_restore_destination_path, archive_name, jenkins_home, persist_tmp_archive):

    # Untar the archive file in the tmp_directory
    tar = tarfile.open(f'{tmp_restore_destination_path}/{archive_name}')
    jenkins_home_dir_name = tar.getnames()[0]
    tar.extractall(f'{tmp_restore_destination_path}')
    tar.close()

    # Before we replace the jenkins_home with the extracted directory to, check if there is a  jenkins_home
    # directory in the tmp_jenkins_home (one directory up to the user specified or default jenkins_home)
    # then rename to jenkins_home-time.time()
    tmp_jenkins_home = str(Path(jenkins_home).parents[0])
    old_jenkins_home = f"{tmp_jenkins_home}/{jenkins_home_dir_name}_{time.time()}"
    if os.path.exists(jenkins_home):
        shutil.move(jenkins_home, old_jenkins_home)
        shutil.move(f"{tmp_restore_destination_path}/{jenkins_home_dir_name}", tmp_jenkins_home)

    # If persist_tmp_archive is false, delete the temporary directory
    if persist_tmp_archive is False:
        try:
            shutil.rmtree(tmp_restore_destination_path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    # Restore success message
    restore_msg = f""" Jenkins restore is successful,
         
        The Restore Archive Name = {archive_name}
        Path to Old Jenkins Home = {old_jenkins_home}
        Path to New Jenkins Home = {tmp_jenkins_home}/{jenkins_home_dir_name}

        Happy CI/CD!!!"""

    # Let user know the result,
    click.secho(restore_msg, fg='green')


def local_tarfile_restore(archive_name, restore_archive_path, jenkins_home, persist_tmp_archive):
    """
    local_tarfile_restore creates a directory called jenkins_backup_restore_cli_{time.time()}, uses the
    user specified path given with --restore-archive-path (or defaults to the os.getcwd()) to find the
    tar file and move it in to that directory. Once the file is moved it extracts the tar file in that
    temporary directory. It will also check for the jenkins_home directory (defaults to /var/jenkins_home,
    unless user specified a path through --jenkins-home-dir) and rename the jenkins_home to
    jenkins_home_{time.time()} and move the extracted file to the /var(default path) and remove the
    temporary directory.

    :param archive_name
    :param restore_archive_path
    :param jenkins_home
    :param persist_tmp_archive
    :return:
    """

    if restore_archive_path:

        # Expand the path if ~ is used
        restore_archive_full_path = os.path.expanduser(f'{restore_archive_path}')

        # Set a tmp restore path
        tmp_restore_destination_path = restore_archive_full_path + f"/jenkins_backup_restore_cli_{time.time()}"

        # Create the tmp_directory
        _make_tmp_dir(tmp_restore_destination_path, restore_archive_path)

        if not os.path.exists(f"{restore_archive_full_path}/{archive_name}"):
            # throws an exception
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{restore_archive_full_path}/{archive_name}")
        else:
            # Move the tar file to the tmp_backup_destination_path
            shutil.copy(f"{restore_archive_full_path}/{archive_name}", tmp_restore_destination_path)

        try:
            # Untar the archive
            _untar_archive_replace_jenkins_home(tmp_restore_destination_path, archive_name, jenkins_home, persist_tmp_archive)
        except OSError as e:
            shutil.rmtree(tmp_restore_destination_path)
            print("Error: %s - %s, deleted the %s temporary directory" % (e.filename, e.strerror, tmp_restore_destination_path))


def remote_tarfile(restore_bucket_name, archive_name, restore_archive_download_path, jenkins_home, persist_tmp_archive):
    """
    remote_tarfile creates a directory called jenkins_backup_restore_cli_{time.time()}, uses the
    user specified path given with --restore-archive-download-path (or defaults to the os.getcwd()) to
    downloads the tar file from an s3 bucket using the bucket name specified by user with --restore-bucket-name
    as save it in to that temporary directory. Once the file is downloaded it extracts the tar file in that
    temporary directory. It will also check for the jenkins_home directory (defaults to /var/jenkins_home,
    unless user specified a path through --jenkins-home-dir) and rename the jenkins_home to
    jenkins_home_{time.time()} and move the extracted file to the /var(default path) and remove the
    temporary directory.

    :param restore_bucket_name
    :param archive_name
    :param restore_archive_download_path
    :param jenkins_home
    :param persist_tmp_archive
    :return:

    For this method to work, the AWS credentials should be preset in the terminal session from where
    ever you are running the jenkins_backup_restore_cli from or the AWS_ACCESS_KEY_ID and ACCESS_SECRET_ACCESS_KEY
    should be set in the ~/.aws/credentials file.
    """
    # Expand the path if ~ is used
    restore_archive_download_full_path = os.path.expanduser(f'{restore_archive_download_path}')

    # Set a tmp restore path to download the archive from s3
    tmp_restore_destination_path = restore_archive_download_full_path + f"/jenkins_backup_restore_cli_{time.time()}"

    # Create the tmp_directory
    _make_tmp_dir(tmp_restore_destination_path, restore_archive_download_path)

    # Create the s3 object and download the backup-archive from the user specified bucket name
    s3_resource = boto3.client('s3')
    try:
        s3_resource.download_file(restore_bucket_name, archive_name, f'{tmp_restore_destination_path}/{archive_name}')
    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    # Untar the archive
    _untar_archive_replace_jenkins_home(tmp_restore_destination_path, archive_name, jenkins_home, persist_tmp_archive)

