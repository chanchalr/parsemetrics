# parsemetrics

a library to parse metrics from files through out commit history.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Docker Build](#docker-build)
  - [Code Examples](#code-examples)

## Getting Started
This is a python library that can parse git commits and look for metrics stored in json format . The library stores metrics and has function to reply metrices. Its written in python3 and uses postgres to store data

### Prerequisites

This library uses python3 with and uses libraries gitpython,psycopg2 and yaml

### Installation

pip3 install -r requirements.txt 
python3 setup.py install


## Usage

We need a postgres installation for this library. A sample docker implementation is present in the library

### Posgres Docker Build

```bash
cd dockers/postgres-metrics/
docker build ./ -t postgresmetrics:latest
```

### Start Postgres Docker

```bash
docker-compose -f docker-compose.yml up -d
```

We need to create a config file that contains directions to connect to database. Following is a sample config file
### Config file
```
database:
  type: "postgres"
  host: localhost
  type: "postgres"
  port: 5432
  dbname: "runmetrics"
  user: postgres
  password: m3tr1cs
```
Once the config file is ready we can invoke library using following code
```
python3
parser = iterative_metrics.metric_parser("./config.yaml")
parser.parse_repo('<repo_path>','<path_to_metrics_file>')
first_commit = parser.fetch_repo_data(count=1)
print(first_commit)
second_commit = parser.fetch_repo_data(commit_id=first_commit[0]["commit_id"],count=1)
print(second_commit)
first_again = parser.fetch_repo_data(commit_id=second_commit[0]["commit_id"],count=1,direction="back")
```

