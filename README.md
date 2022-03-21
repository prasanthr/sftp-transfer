# Copyright 2019 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Sample App for listening to a pub/sub topic (triggered by GCS file upload)
# and transferring the file to an SFTP server
# 
# Sections copied from https://github.com/GoogleCloudPlatform/python-docs-samples
# and https://github.com/googleapis/python-storage/
#

This sample shows how to listen to a pub/sub topic (triggered by GCS file upload)
and transferring the file via SFTP to a different location

To use, fork this repo, Customize main.py to modify the sftp desentiation,
build, tag and push the image to Artifact Repository

Configure a Cloud Run app using this image

## Build the image

```
docker build -t sftp-transfer  .
```

## Push to GCR 

```
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/sftp-transfer

```
