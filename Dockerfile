FROM python:3.8-alpine

ENV VERSION=1.1.9

RUN pip3 install jenkins-backup-restore-cli==${VERSION}