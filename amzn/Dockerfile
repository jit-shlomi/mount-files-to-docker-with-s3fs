################
# ENVs Image
################

FROM public.ecr.aws/amazonlinux/amazonlinux:2 as envs

# Set arguments to be used throughout the image
ARG OPERATOR_HOME="/home/op"
# Bitbucket-pipelines uses docker v18, which doesn't allow variables in COPY with --chown, so it has been statically set where needed.
# If the user is changed here, it also needs to be changed where COPY with --chown appears
ARG OPERATOR_USER="op"
ARG OPERATOR_UID="50000"

# Attach Labels to the image to help identify the image in the future

# Set arguments for access s3 bucket to mount using s3fs
ARG BUCKET_NAME
ARG S3_ENDPOINT="https://s3.us-east-1.amazonaws.com"

# Add environment variables based on arguments
ENV OPERATOR_HOME ${OPERATOR_HOME}
ENV OPERATOR_USER ${OPERATOR_USER}
ENV OPERATOR_UID ${OPERATOR_UID}
ENV BUCKET_NAME ${BUCKET_NAME}
ENV S3_ENDPOINT ${S3_ENDPOINT}


################
# Dist Image
################
FROM envs as dist

RUN yum update -y && yum install -y amazon-linux-extras
RUN amazon-linux-extras enable python3.8
RUN yum install -y shadow-utils python-markupsafe python38 python3-wheel pip git gcc gcc-c++ kernel-devel zlib zlib-devel openssh openssh-clients make python38-devel

# Add user for code to be run as (we don't want to be using root)
RUN useradd -ms /bin/sh -d ${OPERATOR_HOME} --uid ${OPERATOR_UID} ${OPERATOR_USER}

# install s3fs
# install s3fs
RUN yum install -y gcc-c++ fuse fuse-devel automake autoconf git libcurl-devel libxml2-devel openssl-devel


# RUN apk del .build-dependencies

RUN git clone https://github.com/s3fs-fuse/s3fs-fuse.git && \
    cd s3fs-fuse \
    git checkout tags/${S3FS_VERSION} && \
    ./autogen.sh && \
    ./configure --prefix=/usr && \
    make && \
    make install

# setup s3fs configs
RUN echo "s3fs#${BUCKET_NAME} ${OPERATOR_HOME}/s3_bucket fuse _netdev,allow_other,nonempty,umask=000,uid=${OPERATOR_UID},gid=${OPERATOR_UID},passwd_file=${OPERATOR_HOME}/.s3fs-creds,use_cache=/tmp,url=${S3_ENDPOINT} 0 0" >> /etc/fstab
RUN sed -i '/user_allow_other/s/^#//g' /etc/fuse.conf

# Set our user to the operator user
USER ${OPERATOR_USER}
WORKDIR ${OPERATOR_HOME}
COPY main.py .

RUN printf '#!/usr/bin/env sh  \n\
echo ${ACCESS_KEY_ID}:${SECRET_ACCESS_KEY} > ${OPERATOR_HOME}/.passwd-s3fs \n\
chmod 400 ${OPERATOR_HOME}/.passwd-s3fs \n\
mkdir ${OPERATOR_HOME}/s3_bucket \n\
s3fs ${BUCKET_NAME} ${OPERATOR_HOME}/s3_bucket \n\
exec python ${OPERATOR_HOME}/main.py \
# exec /bin/sh \
' >> ${OPERATOR_HOME}/entrypoint.sh

RUN chmod 700 ${OPERATOR_HOME}/entrypoint.sh
ENTRYPOINT [ "/home/op/entrypoint.sh" ]