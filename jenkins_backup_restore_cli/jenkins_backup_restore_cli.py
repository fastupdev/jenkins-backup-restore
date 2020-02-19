import os
import time
import click
import errno
from pyfiglet import Figlet
from jenkins_backup_restore_cli.subscripts.backup import local_tarfile_backup, remote_tarfile_backup
from jenkins_backup_restore_cli.subscripts.restore import local_tarfile_restore, remote_tarfile


# Date as global variable
current_time = time.time()

# Text to render while running the cli
cli_tag = Figlet(font='big')
click.secho(cli_tag.renderText('Jenkins Backup Restore Cli'), fg='blue')


def validate_argument(ctx, param, value):
    if not value:
        raise click.BadParameter('Argument cannot be empty, please specify a path')
    return value


# Using click.group to make the jenkins_backup_restore_cli tool as the main command
@click.group()
@click.version_option(version='1.1.1')
@click.option('--custom-archive-name',
              help='Custom name for the jenkins backup, defaults to (jenkins_backup)',
              default=f'jenkins_backup')
@click.option('--jenkins-home-dir',
              help='Use the flag if jenkins_home location is other than the default path (/var/jenkins_home)',
              callback=validate_argument)
@click.pass_context
def jenkins_backup_restore_cli(ctx, custom_archive_name, jenkins_home_dir):

    archive_name = ''

    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)

    # If the custom_archive_name is specified it will store the value in archive_name
    # or defaults to jenkins_backup_{current_time}.tar.gz
    if custom_archive_name:
        archive_name = custom_archive_name + ".tar.gz"

    ctx.obj['archive_name'] = archive_name

    # Condition block for to find the jenkins_home directory in the right place,
    # At first, the block looks for directory that is user specified,
    if not os.path.exists(jenkins_home_dir):

        # If the user specified directory does not exists, throws a warning message and checks for default directory,
        click.secho(f"WARNING: User specified directory ({jenkins_home_dir}) does not exist, trying to find the default jenkins_home path (/var/jenkins_home)", fg='yellow')

        # Set the default directory value
        default_jenkins_home_dir = "/var/jenkins_home"

        # If the default directory does not exists,
        if not os.path.exists(default_jenkins_home_dir):

            # If the default directory does not exists, throws a warning message and checks for an environment variable,
            click.secho(f"WARNING: The default jenkins_home (/var/jenkins_home) directory does not exist, trying to find the path in the environment variable JENKINS_HOME", fg='yellow')

            # If the environment variable KEY does not exists, raise an error with a message and exit the program
            if os.getenv('JENKINS_HOME') is not None:

                # If the environment variable KEY exists, set the VALUE as a variable.
                jenkins_home = os.getenv('JENKINS_HOME')

                # If the environment variable VALUE path does not exists
                if not os.path.exists(os.path.expanduser(f'{jenkins_home}')):

                    # Echo the error message
                    click.secho(f"WARNING: Environment variable JENKINS_HOME found with {jenkins_home} path, but {jenkins_home} does not exists", fg='yellow')

                    # Error Message
                    click.secho("ERROR: No jenkins_home found", fg='red')

                    # throws an exception
                    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), jenkins_home_dir)

                else:

                    # Let user know it found the path in the environment variable
                    click.secho(f"Found the {jenkins_home} path in environment variable", fg='green')

            else:

                # Let user know it couldn't find the environment variable
                click.secho("Environment variable JENKINS_HOME is not set!", fg='red')
                raise KeyError('JENKINS_HOME') from None

        else:

            # Let user know it found the path in the default path
            click.secho(f"Found the default path for jenkins_home as {default_jenkins_home_dir} directory", fg='green')

            # Set jenkins_home with default path
            jenkins_home = default_jenkins_home_dir
    else:

        # Let user know it found the path in the path specified
        click.secho(f"Found the jenkins_home path as specified in, {jenkins_home_dir} directory", fg='green')

        # Set jenkins_home with user specified path
        jenkins_home = jenkins_home_dir

    # Create an object for the jenkins_home
    ctx.obj['jenkins_home'] = jenkins_home


# backup-local command
@jenkins_backup_restore_cli.command()
@click.option('--backup-destination-path', help='Local path to store the backup', callback=validate_argument)
@click.pass_context
def backup_local(ctx, backup_destination_path):
    local_tarfile_backup(ctx.obj['archive_name'], ctx.obj['jenkins_home'], backup_destination_path)


@jenkins_backup_restore_cli.command()
@click.option('--backup-bucket-name', help='Bucket name to push the backup tar file to s3')
@click.option('--persist-tmp-archive',
              help='Persists(True) or delete(False) the archive, in the temporary path once the archive pushed to s3 bucket, by default it will delete the tmp dir',
              default=False)
@click.pass_context
def backup_s3(ctx, backup_bucket_name, persist_tmp_archive):
    remote_tarfile_backup(ctx.obj['archive_name'], ctx.obj['jenkins_home'], backup_bucket_name, persist_tmp_archive)


@jenkins_backup_restore_cli.command()
@click.option('--restore-archive-path',
              help='Path to the archive in local directory',
              default=f'{os.getcwd()}',
              callback=validate_argument)
@click.option('--persist-tmp-archive',
              help='Persists or delete the archive in the temporary path once the archive is extracted to jenkins_home, by default it will delete the tmp dir',
              default=False)
@click.pass_context
def restore_local(ctx, restore_archive_path, persist_tmp_archive):
    local_tarfile_restore(ctx.obj['archive_name'], restore_archive_path, ctx.obj['jenkins_home'], persist_tmp_archive)


@jenkins_backup_restore_cli.command()
@click.option('--restore-bucket-name',
              help='Bucket name to download the backup tar from s3')
@click.option('--restore-archive-download-path',
              help='Path to save the downloaded archive from an s3 bucket',
              default=f'{os.getcwd()}',
              callback=validate_argument)
@click.option('--persist-tmp-archive',
              help='Persists or delete the archive in the temporary path once the archive is extracted to jenkins_home, by default it will delete the tmp dir',
              default=False)
@click.pass_context
def restore_s3(ctx, restore_bucket_name, restore_archive_download_path, persist_tmp_archive):
    remote_tarfile(restore_bucket_name, ctx.obj['archive_name'], restore_archive_download_path, ctx.obj['jenkins_home'], persist_tmp_archive)


jenkins_backup_restore_cli.add_command(backup_local)
jenkins_backup_restore_cli.add_command(backup_s3)
jenkins_backup_restore_cli.add_command(restore_local)
jenkins_backup_restore_cli.add_command(restore_s3)

if __name__ == '__main__':
    jenkins_backup_restore_cli(obj={})
