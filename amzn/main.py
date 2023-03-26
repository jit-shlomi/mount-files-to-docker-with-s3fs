#!/usr/bin/env python3
import os

if __name__ == "__main__":
    print('Checking mount status')
    if os.path.ismount("s3_bucket/"):
        print("bucket mounted successfully :)")
    else:
        print("bucket not mounted :(")
    print("list s3 directories")
    print(os.listdir("s3_bucket/"))
