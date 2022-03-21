

## SFTP-Copier Cloud Run app 

A sample Cloud Run App in Python to listen to a pub/sub topic (triggered by GCS file upload) and transfer the newly uploaded file to a SFTP location

Sections copied from GCP Documentation - https://github.com/GoogleCloudPlatform/python-docs-samples
and https://github.com/googleapis/python-storage/

Configure a Cloud Run app using this image

Provided as a code-sample, distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND. Please see LICENSE for more details.

## Build the image

```
docker build -t sftp-transfer  .
```

## Build and Push to GCR 

```
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/sftp-transfer

```
