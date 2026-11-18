# Imagem base com Python
FROM python:3.13-slim

# Pasta de trabalho dentro do container
WORKDIR /app

# Instala as dependências primeiro (aproveita o cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da API
COPY app/ ./app/

# Porta em que a API vai rodar
EXPOSE 8000

# Inicia a API aceitando conexões de fora do container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
