FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /Projeto_Remotive_API

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5431

CMD [ "python", "src/__main__.py" ]
 



