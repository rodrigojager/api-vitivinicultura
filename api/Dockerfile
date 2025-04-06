FROM python:3.9-slim

# Instala dependências necessárias para o Playwright e netcat-openbsd
RUN apt-get update && apt-get install -y \
    curl \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release \
    xdg-utils \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mkdocs-render-swagger-plugin
RUN playwright install --with-deps

COPY . .

RUN chmod +x /app/wait-for-it.sh

EXPOSE 8000

CMD ["/app/wait-for-it.sh", "db", "5432", "--", "sh", "-c", "mkdocs build --config-file docs/mkdocs.yml && uvicorn main_api:app --host 0.0.0.0 --port 8000"]

