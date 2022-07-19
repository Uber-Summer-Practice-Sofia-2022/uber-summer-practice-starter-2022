FROM python:3.8-slim

RUN apt-get update && apt-get install -y vim curl

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8080
ENV FLASK_ENV=development
ENV FLASK_APP=server.py
ENV FLASK_PORT=8080

CMD ["python", "server.py"]
