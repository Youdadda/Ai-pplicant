Hello to the Self-RAG, this is a project meant to make a digital version of you, it gets as real as the amount of data source you give it.

## Create your own digital version
1) Create the environment:
```bash
 $ conda create -n Self-RAG python=3.10
```
2) Activate it:
```bash
$ conda activate Self-RAG
```
3) Install the required packages:
```bash
$ cd src/
$ pip install -r ./requirements.txt
```
4) Setup the environement :
```bash
$ cp .env.example .env
```
Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run Docker Compose Services
```bash
$ cd docker
$ cp .env.example .env
```
- update `.env` with your credentials

```bash
$ sudo docker compose up -d
```

## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000