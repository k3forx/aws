#!bin/bash
FUNCTION_NAME="rds_iam_auth"

version=$(aws lambda update-function-code --function-name "${FUNCTION_NAME}" --zip-file fileb://function.zip --publish --profile kanata | jq -r .Version)

aws lambda update-alias --function-name "${FUNCTION_NAME}" --name test --function-version "${version}" --profile kanata

