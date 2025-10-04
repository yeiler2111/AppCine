FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /code

# Copiar requirements
COPY ./requirement.txt /code/requirements.txt

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiar el resto del proyecto
COPY . /code

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
