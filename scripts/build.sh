#!/bin/bash
set -e
set +v

[[ -z $1 ]] && echo "Please provide a build number" && exit 1;
buildNumber=$1

artifactName="pylunchtime-${buildNumber}"
workingDir=$(pwd)

mkdir -p build
python3 -m venv buildvenv
source ./buildvenv/bin/activate
pip install -r requirements.txt
cd ./buildvenv/lib/python3.7/site-packages
zip -r9 "${workingDir}/build/${artifactName}.zip" *
cd "${workingDir}"
zip -ur9 "${workingDir}/build/${artifactName}.zip" app

deactivate
rm -Rf "${workingDir}/buildvenv"