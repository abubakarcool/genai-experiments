## For Google Colab Enterprise experiment 
### first open console.google.com and search Vertex AI and create a project there
### in dashboard Enable all Recommended APIs
### rename the colab file and set the location to us central lova
### written all the code which is in "RAG on VertexAI.ipynb" file 
### it will create stats_index cluster/index in vector search we will be needing its last number of Index endpoint
### check the status_index in vector search after it's status is deployed then do next things 
## if we want to terminate all this instance we created, here are the things we need to do :
#### 1. in cloud storage->buckets->delete bucket
#### 2. in vector search-> undeploy & delete index


## For Local Google Colab experiment 
### first open console.google.com and search Vertex AI and create a project there
### in dashboard Enable all Recommended APIs
### rename the colab file and set the location to us central lova
### create requirements.text
### create .env and write location and created above project ID in it
### install the requirements by running following command anaconda prompt 
```
gcloud init
gcloud auth application-default login
_conda create -n vertexai python=3.10 -y
_conda activate vertexai
pip install -r requirements.txt
python app.py
```