FROM python:3.8-alpine

ENV VERSION=1.0.7

RUN pip3 install jenkins-backup-restore-cli==${VERSION}