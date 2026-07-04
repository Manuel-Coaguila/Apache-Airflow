FROM python:3.12-slim-bookworm

# Instala bash, pytest y dependencias de ODBC
RUN apt-get update && apt-get install -y \
    bash curl gnupg unixodbc unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
