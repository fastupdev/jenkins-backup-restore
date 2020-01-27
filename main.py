import argparse
import datetime
import os
from jenkins.backup import make_tarfile, local_tarfile_copy, remote_tarfile_copy
from jenkins.restore import local_tarfile, remote_tarfile


def main():
	jenkins_home = os.getenv('JENKINS_HOME')
	date = datetime.date.today()

	parser = argparse.ArgumentParser(prog='jenkins', description='Jenkins Backup and Restore Arguments')
	subparsers = parser.add_subparsers(dest='func')

	# Main parsers
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	parser.add_argument('--cn', '--custom-archive-name', help='custom-archive help', dest='custom_archive_name')
	parser.add_argument('command', choices=['backup', 'restore'], help='type has only two values either backup or restore')

	# Sub parsers for the backup
	local_copy_bkp_parser = subparsers.add_parser('bkp-local', help='Local copy of the archive')
	local_copy_bkp_parser.add_argument('-bd', '--backup-destination-path', help='backup destination path', dest='bkp_dest_path')
	s3_copy_bkp_parser = subparsers.add_parser('bkp-s3', help='Push archive to s3')
	s3_copy_bkp_parser.add_argument('-bb', '--backup-bucket-name', help='destination bucket name', dest='bkp_bucket_name')

	# Sub parsers for the restore
	local_copy_rst_parser = subparsers.add_parser('rst-local', help='Local copy of the archive')
	local_copy_rst_parser.add_argument('-rs', '--restore-source-path', help='archive source path', dest='rst_source_path')
	local_copy_rst_parser.add_argument('-rd', '--restore-destination-path', help='destination path defaults to the /var/jenkins_home', dest='rst_dest_path', default='/var/jenkins_home')
	s3_copy_rst_parser = subparsers.add_parser('rst-s3', help='Push archive to s3')
	s3_copy_rst_parser.add_argument('-rb', '--restore-bucket-name', help='destination bucket name', dest='rst_bucket_name')
	s3_copy_rst_parser.add_argument('-adp', '--artifact-destination-path', help='Artifact download path', dest='artifact_dest_path')

	args = parser.parse_args()

	if args.custom_archive_name:
		archive_name = args.custom_archive_name
	else:
		archive_name = f"jenkins-backup-{date}.tar.gz"

	if args.command == 'backup':
		# calling make_tarfile function
		make_tarfile(archive_name, jenkins_home)

		if args.func == 'bkp-local':
			try:
				local_tarfile_copy(archive_name, args.bkp_dest_path)
			except:
				print("Specify the destination location")

		if args.func == 'bkp-s3':
			try:
				remote_tarfile_copy(args.bkp_bucket_name, archive_name)
			except:
				print("Specify the bucket location")
	elif args.command == 'restore':
		if args.func == 'rst-local':
			try:
				local_tarfile(archive_name, args.rst_source_path, args.rst_dest_path)
			except:
				print("Specify the source location")

		if args.func == 'rst-s3':
			#try:
			remote_tarfile(args.rst_bucket_name, archive_name, args.artifact_dest_path, jenkins_home)
			#except:
				#print("Something is wrong with bucketname or archivename or the downloadable path")


main()
