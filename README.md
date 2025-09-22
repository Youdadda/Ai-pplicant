Welcome to the Ai-pplicant project repository, for this project i aim to make the boring tasks as automatic as possible, for now i'm working on the cv to tweak it's contents to match the job requirements for a given post.
Wanna build it on ur machine ? Follow the following instructions:

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