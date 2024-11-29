FROM python:3.13.0-bookworm

RUN apt update && apt install build-essential

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src .
COPY input ./input

ENTRYPOINT ["flask", "--app", "index", "run", "--host=0.0.0.0", "--port=3005"]
