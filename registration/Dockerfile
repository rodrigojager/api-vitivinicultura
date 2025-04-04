# registration/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema, incluindo netcat (nc)
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY registration_app.py .
COPY templates/ ./templates/
COPY db.py .

# Copia o script wait-for-it.sh e torna-o executável
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 8001

CMD ["/wait-for-it.sh", "db", "5432", "--", "uvicorn", "registration_app:app", "--host", "0.0.0.0", "--port", "8001"]
