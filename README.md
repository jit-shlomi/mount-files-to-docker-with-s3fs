# mount-files-to-docker-with-s3fs

In this POC I use [S3FS](https://github.com/s3fs-fuse/s3fs-fuse) to mount files to a docker image from an S3 bucket.

I implemented it in 3 architectures: debian, alpine & amzn.

So we have 3 docker files.

I sed these resources to help me in the process:

* [debian](https://github.com/maxcotec/s3fs-mount/tree/main)
* [alpine](https://hub.docker.com/r/appsoa/docker-alpine-s3fs/dockerfile)

I also went through these resources:

* [s3fs-fuse](https://github.com/s3fs-fuse/s3fs-fuse)
* [docker-s3fs-client](https://github.com/efrecon/docker-s3fs-client)

Also provided, a github workflow file to build all 3 images and run them.

I use 3 environment variables, all stored in github secrets:

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* BUCKET_NAME

also supplied a python script that list the files in a local directory. This directory contains the mounted files from S3.
