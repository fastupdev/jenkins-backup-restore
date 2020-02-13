import click
import datetime
from pyfiglet import Figlet
from .jenkins.backup import make_tarfile, local_tarfile_copy, remote_tarfile_copy
from .jenkins.restore import local_tarfile, remote_tarfile

date = datetime.date.today()

tool_name = Figlet(font='big')
print(tool_name.renderText('Jenkins Backup Restore Cli'))


@click.group()
@click.version_option(version='1.0.7')
@click.option('--custom-archive-name', default='jenkins-backup-DATE.tar.gz', help='Custom name for the jenkins backup')
@click.option('--jenkins-home-dir', help='Custom Jenkins home directory other than the default (/var/jenkins_home)', default='/var/jenkins_home')
@click.pass_context
def jenkins_backup_restore_cli(ctx, custom_archive_name, jenkins_home_dir):

    if custom_archive_name:
        archive_name = custom_archive_name
    else:
        archive_name = f"jenkins-backup-{date}.tar.gz"

    if jenkins_home_dir:
        jenkins_home = jenkins_home_dir

    ctx.obj['archive_name'] = archive_name
    ctx.obj['jenkins_home'] = jenkins_home


@jenkins_backup_restore_cli.command()
@click.option('--bd', '--backup-destination-path', help='Local path to store the backup')
@click.pass_context
def backup_local(ctx, backup_destination_path):
    make_tarfile(ctx.obj['archive_name'], ctx.obj['jenkins_home'])
    local_tarfile_copy(ctx.obj['archive_name'], backup_destination_path)


@jenkins_backup_restore_cli.command()
@click.option('--bb', '--backup-bucket-name', help='Bucket name to push the backup tar file to s3')
@click.pass_context
def backup_s3(ctx, backup_bucket_name):
    make_tarfile(ctx.obj['archive_name'], ctx.obj['jenkins_home'])
    remote_tarfile_copy(backup_bucket_name, ctx.obj['archive_name'])


@jenkins_backup_restore_cli.command()
@click.option('--rs', '--restore-source-path', help='Path to the archive in local directory')
@click.option('--rd', '--restore-path', help='Use the flag if jenkins_home location is other than the default path (/var/jenkins_home)', default='/var/jenkins_home')
@click.pass_context
def restore_local(ctx, restore_source_path, restore_path):
    local_tarfile(ctx.obj['archive_name'], restore_source_path, restore_path)


@jenkins_backup_restore_cli.command()
@click.option('--rb', '--restore-bucket-name', help='Bucket name to download the backup tar from')
@click.option('--adp', '--artifact-destination-path', help='Path to save the downloaded archive from an s3 bucket')
@click.option('--rd', '--restore-path', help='Use the flag if destination path is other than the default path (/var/jenkins_home)', default='/var/jenkins_home')
@click.pass_context
def restore_s3(ctx, restore_bucket_name, artifact_destination_path, restore_path):
    remote_tarfile(restore_bucket_name, ctx.obj['archive_name'], artifact_destination_path, restore_path)


jenkins_backup_restore_cli.add_command(backup_local)
jenkins_backup_restore_cli.add_command(backup_s3)
jenkins_backup_restore_cli.add_command(restore_local)
jenkins_backup_restore_cli.add_command(restore_s3)

if __name__ == '__main__':
    jenkins_backup_restore_cli(obj={})