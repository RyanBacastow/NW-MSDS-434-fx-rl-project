# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, jsonify, request
from google.cloud import storage
import pickle
import os
import numpy as np

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

def list_buckets():
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    mylist = []
    for bucket in buckets:
        mylist.append(bucket.name)

    return mylist


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    out_str = "<br/><h1>Hello Cruel World!</h1>"
    out_str += "<h3>Try out some of this APIs features:</h3>" \
               "<h4>/name/value<br/>/params<br/>/getbuckets<br/>/dir<br/>/predict</h4>"

    return out_str


@app.route('/name/<value>')
def name(value):
    val = {"value": value}
    return jsonify(val)


@app.route('/params', methods=['POST'])
def run_model():
    req_data = request.get_json()
    return req_data


@app.route('/getbuckets')
def get_buckets():
    buck = list_buckets()
    return jsonify(buck)


@app.route('/dir')
def dir():
    files = os.listdir()
    return jsonify(files)  


@app.route('/predict', methods=['POST'])
def predict():

    req_data = request.get_json()
    new_data = np.array([req_data["sepal.length"], req_data["sepal.width"], req_data["petal.length"], req_data["petal.width"]]).astype(float)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket("2020sp-msds-434-dl-sec55-storage")
    blob = bucket.blob("iris_model")

    ## VERY WRONG WAY TO DO THIS
    mod = pickle.loads(blob.download_as_string())
    #val = mod.predict(np.array([[5.1, 3.5, 1.4, 0.2],[4.9, 3. , 1.4, 0.2],[4.7, 3.2, 1.3, 0.2],[4.6, 3.1, 1.5, 0.2],[5. , 3.6, 1.4, 0.2]]))
    val = mod.predict(new_data.reshape(1,-1))

    #return np.array_str(val)
    return list(["Iris-Setosa\n","Iris-Versicolour\n","Iris-Virginica\n"])[val[0]]



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
