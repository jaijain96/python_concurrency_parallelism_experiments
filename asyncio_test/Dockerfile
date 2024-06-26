# syntax=docker/dockerfile:1

FROM centos:latest

WORKDIR /app

COPY requirements.txt requirements.txt

# USER root

RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
# RUN dnf install centos-release-stream -y
# RUN dnf swap centos-{linux,stream}-repos -y
# RUN dnf distro-sync -y

RUN yum clean all
RUN yum -y update
RUN yum install -y python3
RUN yum install -y python3-pip

RUN yum install -y gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel git make

RUN cd /app

RUN curl https://pyenv.run | bash

COPY script0.sh script0.sh

RUN bash script0.sh

# COPY app.py app.py
# CMD [ "/root/.pyenv/shims/python", "-m" , "flask", "run", "--host=0.0.0.0"]
COPY test_batch_async.py test_batch_async.py
CMD [ "/root/.pyenv/shims/python", "-m" , "pytest", "--asyncio-mode", "auto", "test_batch_async.py"]
