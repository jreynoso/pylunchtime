#!/bin/bash
set -e
set +v

[[ -z $1 ]] && echo "Please provide a build number" && exit 1;
buildNumber=$1

# set your AWS config here
awsAccountNo=xxx
awsRegion=us-west-2
artifactBucket=dispassion-ops-lambda-${awsRegion}

artifactKey=pylunchtime
artifactName="${artifactKey}-${buildNumber}.zip"
lambdaName=${artifactKey}

echo "Uploading artifact to S3"
aws s3 cp ./build/"${artifactName}" s3://${artifactBucket}/${artifactKey}/"${artifactName}"

echo "Deploying buildNumber=${buildNumber}"
aws lambda update-function-code \
 --function-name arn:aws:lambda:${awsRegion}:${awsAccountNo}:${lambdaName} \
 --s3-bucket ${artifactBucket} \
 --s3-key ${artifactKey}/"${artifactName}" \
 --region ${awsRegion}

echo "Updating build number tag"
aws lambda tag-resource \
 --resource arn:aws:lambda:${awsRegion}:${awsAccountNo}:function:${lambdaName} \
 --tags BuildNumber="${buildNumber}" \
 --region ${awsRegion}

echo "Publishing version"
aws lambda publish-version --function-name ${lambdaName}

echo "Done"
