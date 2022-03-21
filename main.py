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

# [START cloudrun_pubsub_server_setup]
# [START run_pubsub_server_setup]
import base64
import os
import random
import json

from flask import Flask, request
from google.cloud import storage
import pysftp

app = Flask(__name__)
@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    message = "<MESSAGE>"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        message = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        #message =  envelope["message"]["data"]

    print(f"Message: {message}!")
    
    message_dict  = json.loads(message)
    bucket_name = message_dict["bucket"]
    source_blob_name = message_dict["name"]
    temp_localfile = "/tmp/tmpfile" + str(random.randint(0,100))
    print(f"bucket_name: {bucket_name}!")
    print(f"source blob name: {source_blob_name}!")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(temp_localfile)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, temp_localfile
        )
    )

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(os.getenv("SFTP_SERVER"), username=os.getenv("SFTP_USER"), 
                private_key='/key/sftp-private-key', cnopts = cnopts) as sftp:
            sftp.put(temp_localfile)

    print ("file copied to sftp server")

    return ("", 204)


# [END run_pubsub_handler]
# [END cloudrun_pubsub_handler]


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
    