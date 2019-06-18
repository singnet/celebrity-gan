FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

ARG git_owner
ARG git_repo
ARG git_branch

ENV SINGNET_REPOS=/opt/singnet
ENV PROJECT_ROOT=${SINGNET_REPOS}/${git_repo}
ENV SERVICE_DIR=${PROJECT_ROOT}/service
ENV PYTHONPATH=${SERVICE_DIR}

## Installing common dependencies and python3-pip
RUN apt-get update && \
    apt-get install -y wget curl nano git python3-dev python3-pip && \
    python3 -m pip install --upgrade pip && \
    ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1 && \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs/:$LD_LIBRARY_PATH && \
    rm /usr/local/cuda/lib64/stubs/libcuda.so.1

# Installing snet-daemon + dependencies
RUN SNETD_VERSION=`curl -s https://api.github.com/repos/singnet/snet-daemon/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")'` && \
    cd /tmp && \
    wget https://github.com/singnet/snet-daemon/releases/download/${SNETD_VERSION}/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    mv snet-daemon-${SNETD_VERSION}-linux-amd64/snetd /usr/bin/snetd

# Cloning service repository and downloading models
RUN mkdir -p ${SINGNET_REPOS} && \
    cd ${SINGNET_REPOS} &&\
    git clone -b ${git_branch} https://github.com/${git_owner}/${git_repo}.git &&\
    cd ${PROJECT_ROOT} &&\
    python3 -m pip install -r requirements.txt &&\
    sh buildproto.sh

RUN cd ${SERVICE_DIR} &&\
#    export PYTHONPATH=${SERVICE_DIR} &&\
    export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu:/usr/local/cuda-9.0/lib64:${LD_LIBRARY_PATH}" &&\
    chmod +x import_example.py
#    python3 import_example.py

WORKDIR ${PROJECT_ROOT}