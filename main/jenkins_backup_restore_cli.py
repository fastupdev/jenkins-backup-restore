import argparse
import datetime
import os
from jenkins.backup import make_tarfile, local_tarfile_copy, remote_tarfile_copy
from jenkins.restore import local_tarfile, remote_tarfile
from pyfiglet import Figlet


def main():
	f = Figlet(font='slant')
	print(f.renderText('Jenkins Backup Restore Cli'))

	jenkins_home = os.getenv('JENKINS_HOME')
	date = datetime.date.today()

	parser = argparse.ArgumentParser(prog='jenkins-backup-restore-cli', description='Jenkins Backup and Restore Arguments')
	subparsers = parser.add_subparsers(dest='func')

	# Main parsers
	parser.add_argument('--v', '--version', action='version', version='%(prog)s 1.0.5')
	parser.add_argument('--cn', '--custom-archive-name', help='Give the backup a custom name ', dest='custom_archive_name')
	parser.add_argument('command', choices=['backup', 'restore'], help='use either backup to backup or use restore to restore')

	# Sub parsers for the backup
	local_copy_bkp_parser = subparsers.add_parser('backup-local', help='Save the archive to a local directory')
	local_copy_bkp_parser.add_argument('-bd', '--backup-destination-path', help='Local path to store the backup', dest='bkp_dest_path')
	s3_copy_bkp_parser = subparsers.add_parser('backup-s3', help='Push the archive to an s3 bucket')
	s3_copy_bkp_parser.add_argument('-bb', '--backup-bucket-name', help='Bucket name to push an archive to s3', dest='bkp_bucket_name')

	# Sub parsers for the restore
	local_copy_rst_parser = subparsers.add_parser('restore-local', help='Restore archive from a local directory')
	local_copy_rst_parser.add_argument('-rs', '--restore-source-path', help='Path to the archive in local directory', dest='rst_source_path')
	local_copy_rst_parser.add_argument('-rd', '--restore-destination-path', help='If destination path is other than the default path (/var/jenkins_home)', dest='rst_dest_path', default='/var/jenkins_home')
	s3_copy_rst_parser = subparsers.add_parser('restore-s3', help='Pull an archive from an s3 bucket to a specific location and restore it')
	s3_copy_rst_parser.add_argument('-rb', '--restore-bucket-name', help='Bucket name to download the archive from', dest='rst_bucket_name')
	s3_copy_rst_parser.add_argument('-adp', '--artifact-destination-path', help='Path to save the downloaded archive from an s3 bucket', dest='artifact_dest_path')

	args = parser.parse_args()

	if args.custom_archive_name:
		archive_name = args.custom_archive_name
	else:
		archive_name = f"jenkins-backup-{date}.tar.gz"

	if args.command == 'backup':
		# calling make_tarfile function
		make_tarfile(archive_name, jenkins_home)

		if args.func == 'backup-local':
			try:
				local_tarfile_copy(archive_name, args.bkp_dest_path)
			except:
				print("Specify the destination location")

		if args.func == 'backup-s3':
			try:
				remote_tarfile_copy(args.bkp_bucket_name, archive_name)
			except:
				print("Specify the bucket location")
	elif args.command == 'restore':
		if args.func == 'restore-local':
			try:
				local_tarfile(archive_name, args.rst_source_path, args.rst_dest_path)
			except:
				print("Specify the source location")

		if args.func == 'restore-s3':
			try:
				remote_tarfile(args.rst_bucket_name, archive_name, args.artifact_dest_path, jenkins_home)
			except:
				print("Something is wrong with bucketname or archivename or the downloadable path")


if __name__ == "__main__":
	main()
