#!/usr/bin/env bash

# remove function.zip if already exists
rm function.zip

# create package directory (-p for suppressing error if directory already exists)
mkdir -p package

cd package

# Install packages from requirements.lambda.txt
pip3 install -r ../requirements.txt --target .

# zip the library dependency
zip -r9 ../function.zip .

cd -

# Add lambda_function.py to the zipped folder
zip -g function.zip lambda_function.py
zip -g function.zip rds-ca-2019-root.pem

# Remove the package folder after function.zip is created successfully
rm -rf package
