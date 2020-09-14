#!bin/bash
FUNCTION_NAME="rds-iam-auth"
ROLE="arn:aws:iam::411479233930:role/lambda-role-for-rds"

# aws lambda update-function-configuration --function-name "${FUNCTION_NAME}" --role "${ROLE}"
version=$(aws lambda update-function-code --function-name "${FUNCTION_NAME}" --zip-file fileb://function.zip --publish --profile admin-kanata | jq -r .Version)

aws lambda update-alias --function-name "${FUNCTION_NAME}" --name dev --function-version "${version}" --profile admin-kanata

