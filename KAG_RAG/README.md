# KAG (Knowledge Augmented Generation)
# it is framework which integrates large language models (LLMs) with structured knowledge graphs to enable logical reasoning and question-answering in specialized domains.
## it work on :
 - Open Information EXtraction (OpenIE)
 - Knowledge Graphs (KGs)
 - Advanced multi-hops reasoning

## It uses "Symmbolic Logic Reasoning" solving porblem step by step by using logic(rules relationships) instead of plain text.
## e.g. 
## Question : Who is grandfather of John ?
## (John) -> hasfather -> (Mark)
## (Mark) -> hasfather -> (David)
## Answer : David.

## It uses "Structured Knowledge" like graphs, tables instead of plain text.
## It breaks info 3 parts which are called : "Semantic Triples & Entities".
### (1)Subject -> (2)Predicate -> (3)Object
## e.g. 
## (Elon Musk)  -> founded  -> (SpaceX)
##              -> CEO of   -> (Tesla)
##              -> Born     -> (South Africa)

 - - 

## Tutorial from this website : https://openspg.yuque.com/ndx6g9/docs_en/rs7gr8g4s538b1n7#cikso
### We need OpenSPG Server running in Docker container, as KAG doesn’t fully self-host everything in Python process: it still needs an OpenSPG-Server instance running to handle metadata, schema management, graph storage, reasoning calls and image storage.
### download docker and install with WSL 2 (Windows SubSystem Linux)
### Use the following commands to download the docker-compose.yml file and launch the services with Docker Compose.
```bash
$env:HOME = $env:USERPROFILE

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/OpenSPG/openspg/refs/heads/master/dev/release/docker-compose-west.yml" -OutFile "docker-compose-west.yml"
docker compose -f docker-compose-west.yml up -d  // (make sure the windows docker application working background)
docker ps
open http://127.0.0.1:8887  // (open inside browser)
```


### Enable UTF-8 support globally on Windows : 
 - If you want to fix the root cause and let Python print Chinese/Unicode properly:
 - Go to Control Panel > Region > Administrative > Change system locale.
 - Check the box for “Beta: Use Unicode UTF-8 for worldwide language support”.
 - Restart your system.

### change YAML configuration file anywhere if we found with openai details :-
```bash
#--- cd kag/examples/medicine for file "kag_config.yaml"
#------------project configuration start----------------#
openie_llm: &openie_llm
  api_key: 
    sk-proj-xxxx12312312312312131231212312321123123212321321xxxx
  base_url: https://api.openai.com/v1
  model: gpt-4
  type: openai
  max_tokens: 2048

chat_llm: &chat_llm
  api_key: 
    sk-proj-xxxx12312312312312131231212312321123123212321321xxxx
  base_url: https://api.openai.com/v1
  model: gpt-4
  type: openai
  max_tokens: 2048

vectorize_model: &vectorize_model
  api_key: 
    sk-proj-xxxx12312312312312131231212312321123123212321321xxxx
  base_url: https://api.openai.com/v1
  model: text-embedding-3-large
  type: openai
  vector_dimensions: 3072
vectorizer: *vectorize_model
```

## Initialize the KAG project
```bash
knext project restore --host_addr http://127.0.0.1:8887 --proj_path .
```
### Commit the Schema
```bash
knext schema commit
```
### Build the Knowledge Graph
```bash
cd builder
python indexer.py
cd ..
```
### Inspect with GQL
```bash
knext reasoner execute --dsl "
MATCH
  (d:Medicine.Disease)-[r]->(t)
RETURN
  d.id, d.name, r, t
"
```
### Run the Demo Question Answer 
```bash
cd solver
python evaForMedicine.py
cd ..
```
### Cleanup if required 
```bash
rm -rf builder/ckpt
curl "http://127.0.0.1:8887/project/api/delete?projectId=1"
```

 - - 

## How it all works :-
## 1. Spinning OpenSPG Server
### OpenSPG is the backend graph‐database and schema‐management service that KAG uses to :-
 - Store knowledge graph (nodes, edges, properties)
 - Manage schema (entity types, relation types)
 - Execute GQL queries (ISO-compliant graph queries)
### Serve as the bridge between KAG’s builder/solver pipelines and persistent storage

## 2. Project Initialization 
### it reads local kag_config.yaml configurations/settings and save these to OpenSPG under some project-ID and uploads the metadata which tells the server how to talk to which specific LLM, embedding model etc, when the builder/solver tasks run.

## 3. Commit Schema
### It Reads corresponding e.g. schema/Medicine.schema (this is a DSL defining entity types like Medicine.Disease, relation types like Medicine.hasSymptom, and the properties each node/edge carries) Tells the OpenSPG server “Here’s the blueprint of our graph” so it can create the corresponding tables/indexes or internal graph-structures.

## 4. Build the Knowledge Graph
### It is the populate or data filling step in which it does 2 things :
 - Structured import : Reads CSV files in builder/data/*.csv ; according to the builder chains in your config, imports each row as nodes/edges in the graph.
 - Schema-free extraction : Send unstructured text through the LLM “openie_llm” to extract triples (subject, predicate, object), Post-processes them and writes them into graph under the schema we committed above

## 5. Inspect with GQL
### It’s executing GQL directly on the data that our schema.
```bash
MATCH (d:Medicine.Disease)-[r]->(t) RETURN d.name, type(r), t.name
```

## 6. Run the Demo Question Answer
 - Loads your same kag_config.yaml and connects to the graph
 - Takes a hard-coded or interactive natural‐language question (e.g. “What are common symptoms of Disease X?”)
 - Planner + Executor pipelines translate that question into graph traversals, invoke the LLM as needed, merge graph‐retrieved facts, and then produce a final answer plus step-by-step trace.
