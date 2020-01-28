# Python Jenkins Backup Restore Module

[![PyPI - Downloads](https://img.shields.io/pypi/dm/jenkins-backup-restore-cli?style=plastic)](https://pypi.org/project/jenkins-backup-restore-cli/)
[![PyPI - Version](https://img.shields.io/pypi/v/jenkins-backup-restore-cli?style=plasticl&logo=pypi)](https://pypi.org/project/jenkins-backup-restore-cli/)

Jenkins-backup-restore module takes a backup of the jenkins home directory and restores it.

#### Backup

Following are the list of items that the backup module can do,

1. Look for the JENKINS_HOME env values (or use the default /var/jenkins_home). Export JENKINS_HOME, if does not exists.
2. Take a backup of the jenkins_home with tar and stores it in current directory (default: /var/jenkins_home)
3. Move the backup tar to a specific folder locally (optional with flags).
4. Push the backup tar to a specific bucket in S3 (optional with flags). 

#### Restore
Following are the list of items that the restore module can do,

1. Look for the binary in the local file system in the specific destination path.
2. Extract the tar file to JENKINS_HOME path (default: /var/jenkins_home)
3. Look for the a artifact binary in the s3 given a specific bucket name and download it in the current directory unless a specific artifact destination path is given. (optional with flags)
4. Extract the tar file to JENKINS_HOME path (default: /var/jenkins_home)

#### Installation
Run the following command to install the jenkins-backup-restore tool,
```
pip3 install jenkins-backup-restore-cli
```

#### Backup and Restore Arguments:
Once the binary is installed with pip3, use the following command line argument to either take a backup or restore the existing backup.
 
```
    --v, --version                      Show program's version number

    --cn, --custom-archive-name         Give the backup a custom name
    
    # backup to a local dir command and argument
    backup-local                        Save the archive to a local directory
    -bd, --backup-destination-path,     Local path to store the backup
    
    # backup to s3 command and argument
    backup-s3                           Push the archive to an s3 bucket
    -bb, --backup-bucket-name,          Bucket name to push an archive to s3
    
    # restore archive from a local directory 
    restore-local                        Restore archive from a local directory
    -rs, --restore-source-path           Path to the archive in local directory
    -rd, --restore-destination-path      If destination path is other than the default path (/var/jenkins_home)
    
    # restore archive from an s3 bucket
    restore-s3                           Pull an archive from an s3 bucket to a specific location and restore it
    -rb, --restore-bucket-name           Bucket name to download the archive from
    -adp, --artifact-destination-path    Path to save the downloaded archive from an s3 bucket

  {backup,restore}                       use either backup to backup or use restore to restore
```

#### Examples

To give a custom name to the backup
```
jenkins-backup-restore-cli backup-local --cn <custom-name.tar.gz> backup
```
> If `--backup-destination-path` not specified, stores in the current directory.

To backup jenkins to local directory,
```
jenkins-backup-restore-cli backup-local --backup-destination-path <custom-dir> backup
```

To backup jenkins to an s3 bucket,
```
jenkins-backup-restore-cli backup-local --backup-bucket-name <bucket-name> backup
```

To restore an archive from local path,
```
jenkins-backup-restore-cli restore-local --restore-source-path <archive-path> restore
```

To restore an archive from an s3 bucket,
```
jenkins-backup-restore-cli restore-s3 --restore-bucket-name <bucket-name> --artifact-destination-path <path-to-download-in-local> restore
```
