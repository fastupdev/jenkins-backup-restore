Python Jenkins Backup Restore Module
====================================

|PyPI - Downloads| |PyPI - Version| |PyPI - Status| |CircleCI - Build|
|Docker| |Libraries-Rank|

jenkins-backup-restore-cli module takes a backup of the jenkins home directory and restores it as required.

::

         _            _    _             ____             _
        | |          | |  (_)           |  _ \           | |
        | | ___ _ __ | | ___ _ __  ___  | |_) | __ _  ___| | ___   _ _ __
    _   | |/ _ \ '_ \| |/ / | '_ \/ __| |  _ < / _` |/ __| |/ / | | | '_ \
   | |__| |  __/ | | |   <| | | | \__ \ | |_) | (_| | (__|   <| |_| | |_) |
    \____/ \___|_| |_|_|\_\_|_| |_|___/ |____/ \__,_|\___|_|\_\\__,_| .__/
                                                                    | |
                                                                    |_|
    _____           _                    _____ _ _
   |  __ \         | |                  / ____| (_)
   | |__) |___  ___| |_ ___  _ __ ___  | |    | |_
   |  _  // _ \/ __| __/ _ \| '__/ _ \ | |    | | |
   | | \ \  __/\__ \ || (_) | | |  __/ | |____| | |
   |_|  \_\___||___/\__\___/|_|  \___|  \_____|_|_|

Prerequisites
-------------

-  python2.7 or higher
-  pip or pip3

Installation
------------

Run the following command to install the jenkins-backup-restore-cli,

::

   pip3 install jenkins-backup-restore-cli

What does it do?
----------------

The jenkins-backup-restore-cli tool will backup the jenkins_home
directory as well as restores it.

Backup
^^^^^^

-  The backup module will look for a jenkins-home directory
-  Tar it into a temporary directory.
-  Copy the tarfile to an user specified location or to a AWS s3 bucket.
-  Delete the temporary directory (can be persisted with
   ``--persist-tmp-archive``)

Restore
^^^^^^^

-  The restore module will look for a jenkins-home directory that needs
   to be restored
-  create a tmp directory and copy the tarfile or download the tarfile
   from an s3 bucket to it.
-  Untar the tarfile in that temporary directory
-  Make a copy of existing jenkins_home directory
-  Replace the old jenkins_home with the untarred jenkins_home
-  Delete the temporary directory


Backup and restore
------------------

jenkins-backup-restore-cli common options for both backup and restore,

Common Options
^^^^^^^^^^^^^^

.. _--version:

``--version``
'''''''''''''

Shows version number of the package

::

   jenkins-backup-restore-cli --version

.. _--custom-archive-name:

``--custom-archive-name``
'''''''''''''''''''''''''

To create a backup tarfile with the custom name,

::

   jenkins-backup-restore-cli --custom-archive-name my-backup

..

   Note: If not provided, it will backup with the default name (default:
   jenkins_backup.tar.gz)

.. _--jenkins-home-dir:

``--jenkins-home-dir``
''''''''''''''''''''''

-  user should provide a ``--jenkins-home-dir``.
-  If the user specified directory does not exists, tool looks for a
   default location (default: ``/var/jenkins_home``)
-  If the default location does not exists, the tool will look for an
   ``JENKINS_HOME`` environment variable.

::

   jenkins-backup-restore-cli --jenkins-home-dir /var/lib/jenkins

..

   Note: In above each step the tool will throw a warning and throws an
   error if environment variable does not exists or the path set in the
   value does not exists.

Commands
~~~~~~~~

Backup Commands
^^^^^^^^^^^^^^^

To backup jenkins_home, either one of the following commands with
arguments can be used,

-  ``backup-local`` - Take a backup in the local machine (same machine
   where jenkins is running)

   -  ``--backup-destination-path``, local path to store the backup

::

   jenkins-backup-restore-cli --jenkins-home-dir <jenkins_home> backup-local --backup-destination-path <local-path>

-  ``backup-s3`` - Take a backup and push it to an s3 bucket

   -  ``--backup-bucket-name``, s3 bucket name to store the backup.
   -  ``--persist-tmp-archive``, persists(True) or delete(False) the
      archive, in the temporary path once the archive pushed to s3
      bucket (default: ``False``)

::

   jenkins-backup-restore-cli --jenkins-home-dir <jenkins_home> backup-s3 --backup-bucket-name <bucket-name> --persist-tmp-archive True

Restore Commands
^^^^^^^^^^^^^^^^

To restore jenkins_home, either one of the following commands with
arguments can be used,

-  ``restore-local`` - Restore from a local jenkins backup tarfile

   -  ``--restore-archive-path``, local path to the backup tarfile
   -  ``--persist-tmp-archive``, persists(True) or delete(False) the
      archive in the temporary path once the archive is extracted to
      jenkins_home (default: ``False``)

::

   jenkins-backup-restore-cli --jenkins-home-dir <jenkins_home> restore-local --restore-archive-path <path-to-backup-tarfile> --persist-tmp-archive True

-  ``restore-s3`` - Restore from a s3 bucket

   -  ``--restore-bucket-name``, bucket name to download the archive
      from
   -  ``--restore-archive-download-path``, local path to download the
      archive from s3 bucket
   -  ``--persist-tmp-archive``, persists(True) or delete(False) the
      archive in the temporary path once the archive is extracted to
      jenkins_home (default: ``False``)

::

   jenkins-backup-restore-cli --jenkins-home-dir <jenkins_home> restore-s3 --restore-bucket-path <bucket-name> --restore-archive-download-path <local-path-to-download-tarfile> --persist-tmp-archive True

..

   Note: For any help, use ``--help`` flag.

Dockerfile
----------

A `Dockerfile`_ that has the jenkins-backup-restore-cli latest package
installed on it.

Helm Chart
----------

A Helm chart for the jenkins-backup-restore-cli tool to perform backup
and restore on Jenkins pod running in a Kubernetes cluster, find a
README.md `here`_.

Contributions
-------------

|GitHub - Commits| |GitHub - PRs|

All source code is hosted on `GitHub`_. Contributions are welcome. Contribution Guide `here <CONTRIBUTING.md>`__

Happy CI/CD!! 🚀

.. _Dockerfile: Dockerfile
.. _here: jenkins-backup-restore-cli-chart/README.md
.. _GitHub: https://github.com/fastupdev/jenkins-backup-restore


.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/jenkins-backup-restore-cli?style=plastic
   :target: https://pypi.org/project/jenkins-backup-restore-cli/
.. |PyPI - Version| image:: https://img.shields.io/pypi/v/jenkins-backup-restore-cli?style=plasticl&logo=pypi
   :target: https://pypi.org/project/jenkins-backup-restore-cli/
.. |PyPI - Status| image:: https://img.shields.io/pypi/status/jenkins-backup-restore-cli?style=plasticl&logo=pypi
   :target: https://img.shields.io/pypi/status/jenkins-backup-restore-cli
.. |CircleCI - Build| image:: https://img.shields.io/circleci/build/gh/fastupdev/jenkins-backup-restore?style=plastic&logo=circleci
   :target: https://img.shields.io/circleci/build/gh/fastupdev/jenkins-backup-restore
.. |Docker| image:: https://img.shields.io/docker/pulls/fastdevup/jenkins-backup-restore-cli?style=plastic&?logo=docker
   :target: https://img.shields.io/docker/pulls/fastdevup/jenkins-backup-restore-cli
.. |Libraries-Rank| image:: https://img.shields.io/librariesio/sourcerank/pypi/jenkins-backup-restore-cli.svg?logo=koding&logoColor=white
   :target: https://libraries.io/pypi/jenkins-backup-restore-cli
.. |GitHub - Commits| image:: https://img.shields.io/github/commit-activity/m/fastupdev/jenkins-backup-restore.svg?logo=git&logoColor=white
   :target: https://github.com/fastupdev/jenkins-backup-restore/graphs/commit-activity
.. |GitHub - PRs| image:: https://img.shields.io/github/issues-pr-closed/fastupdev/jenkins-backup-restore.svg?logo=github&logoColor=white
   :target: https://github.com/fastupdev/jenkins-backup-restore/pulls