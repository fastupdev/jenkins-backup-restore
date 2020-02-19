"""backup.py with _make_tmp_dir_and_move_tar_to_tmp, local_tarfile_backup, remote_tarfile_backup takes backup jenkins_home"""
import os
import shutil
import tarfile
import time
import boto3
import click


def _make_tmp_dir_and_move_tar_to_tmp(tmp_backup_destination_path, archive_name, jenkins_home):

    # Create the tmp_directory
    try:
        os.makedirs(tmp_backup_destination_path)
    except OSError:
        print("Creation of the directory %s failed" % tmp_backup_destination_path)

    # Create the tar file with all the contents in the jenkins_home directory
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(jenkins_home, arcname=os.path.basename(jenkins_home))

    # Move the tar file to the tmp_backup_destination_path
    shutil.move(archive_name, tmp_backup_destination_path)

    backup_msg = f""" Jenkins backup is successful,
    Backup Path = {tmp_backup_destination_path}
    Backup File Name = {archive_name}
    
    Happy Restore!!!"""

    # Let user know the result,
    click.secho(backup_msg, fg='green')


def local_tarfile_backup(archive_name, jenkins_home, backup_destination_path):
    """
    local_tarfile_copy creates a directory called jenkins_backup_restore_cli_{time.time()} and move
    the tar file in to that directory. If the --backup-destination-path is specified it will create the
    jenkins_backup_restore_cli_{time.time()} directory in the user specified path and move the to that path.

    :param archive_name:
    :param jenkins_home:
    :param backup_destination_path
    :return:
    """

    # If --backup-destination-path is specified by user
    if backup_destination_path:
        # set a tmp backup path
        tmp_backup_destination_path = os.path.expanduser(f'{backup_destination_path}') + f"/jenkins_backup_restore_cli_{time.time()}"

        # Make the tmp directory in the tmp path, tar the jenkins_home and move it in to
        # the user specified path
        _make_tmp_dir_and_move_tar_to_tmp(tmp_backup_destination_path, archive_name, jenkins_home)

    else:
        # Get current directory
        current_path = os.getcwd()

        # Set a tmp backup path
        tmp_backup_destination_path = current_path + f"/jenkins_backup_restore_cli_{time.time()}"

        # Make the tmp directory in the tmp path, tar the jenkins_home and move it in to
        # the directory created in the current working directory.
        _make_tmp_dir_and_move_tar_to_tmp(tmp_backup_destination_path, archive_name, jenkins_home)


def remote_tarfile_backup(archive_name, jenkins_home, backup_bucket_name, persist_tmp_archive):
    """
    remote_tarfile_copy create temporary dir in the current path and move the tar to it and then push
    the archive to the s3 bucket. For this method to work, the AWS credentials should be pre-set either
    in the terminal session or in the ~/.aws/credentials file from the machine you are running the
    jenkins_backup_restore_cli from. Once the archive is pushed to s3 from the temporary directory,
    by default it will delete the temporary directory unless user specified --persist-tmp-archive flag.

    :param jenkins_home:
    :param archive_name:
    :param backup_bucket_name
    :param persist_tmp_archive
    :return:
    """
    # Get current directory
    current_path = os.getcwd()

    # Set a tmp backup path
    tmp_backup_destination_path = current_path + f"/jenkins_backup_restore_cli_{time.time()}"

    # Make the tmp directory in the tmp path, tar the jenkins_home and move it in to
    # the directory created in the current working directory.
    _make_tmp_dir_and_move_tar_to_tmp(tmp_backup_destination_path, archive_name, jenkins_home)

    # Create s3 object and move the archive to the user specified s3 bucket.
    s3_resource = boto3.resource('s3')
    s3_resource.Object(backup_bucket_name, archive_name).upload_file(Filename=archive_name)

    if persist_tmp_archive is False:
        try:
            shutil.rmtree(tmp_backup_destination_path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
