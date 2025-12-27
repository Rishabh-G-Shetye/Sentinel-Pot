FROM python:3.11-slim
# Install tcpdump for packet capture
RUN apt-get update && apt-get install -y tcpdump && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501 2222 8080