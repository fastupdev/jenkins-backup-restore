#!/bin/bash

current_dir=$PWD/functional-tests-tmp-dir
jenkins_home_path=$current_dir/jenkins_home
tmp_dir=$PWD/tmp

function _make_dirs() {
  mkdir -pv "$jenkins_home_path"
  mkdir -pv "$jenkins_home_path"/jenkins-test-dir{1..5}
}

function _make_dummy_files() {
  touch "$jenkins_home_path"/jenkins-test{1..10}.xml
  touch "$jenkins_home_path"/jenkins-test{1..5}.html
}

function _install_cli_pakcage() {
  echo "export PATH=/root/.local/bin:$PATH" >> $BASH_ENV
  source $BASH_ENV
  python setup.py install --user
}

# Creating dummy jenkins_home and running the tests
function prereq_install() {
  _make_dirs
  _make_dummy_files
  _install_cli_pakcage
}

function backup_local_test(){
  jenkins-backup-restore-cli --jenkins-home-dir "$jenkins_home_path" backup-local --backup-destination-path "$tmp_dir"
}

function restore_local_test() {
  backup_dir=$(ls $tmp_dir)
  jenkins-backup-restore-cli --jenkins-home-dir "$jenkins_home_path" restore-local --restore-archive-path "$tmp_dir"/"$backup_dir"
}
