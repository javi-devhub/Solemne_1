# Etapa 1: Build (compilación de dependencias)
FROM python:3.12-alpine AS builder

WORKDIR /app

# Instalar compiladores y librerías necesarias para compilar dependencias
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libxml2-dev \
    libxslt-dev \
    python3-dev \
    build-base

# Copiar requirements y compilarlos en carpeta temporal
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Etapa 2: Runtime (ejecución ligera)
FROM python:3.12-alpine

WORKDIR /app

# Copiar dependencias ya compiladas desde la etapa builder
COPY --from=builder /install /usr/local

# Copiar solo el código del proyecto
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

