# Ejecución del Proyecto

Este proyecto puede ejecutarse de dos maneras:

1. **Con Docker**, utilizando los contenedores definidos en `docker-compose.yml`.
2. **Localmente con Python (venv)**, configurando las variables de entorno para usar los servicios reales de base de datos y Redis.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.8+](https://www.python.org/downloads/) (solo si vas a ejecutar el proyecto sin Docker)

Verifica tus versiones con:

```bash
docker --version
docker compose version
python --version
```

---

# Ejecución con Docker

Este método permite levantar el entorno completo (API, base de datos y Redis) sin necesidad de instalar dependencias manualmente.

## 1. Construir las imágenes
```bash
docker compose build
```

## 2. Levantar los contenedores
```bash
docker compose up
```

## 3. Levantar en segundo plano (modo detached)
```bash
docker compose up -d
```

## 4. Ver logs
```bash
docker compose logs -f
```

## 5. Detener los contenedores
```bash
docker compose down
```

## 6. Reconstruir completamente (si cambiaste dependencias o variables)
```bash
docker compose up --build
```

---

## Archivo `docker-compose.yml` de referencia

---

## Acceso a los servicios

- API: [http://localhost:8000](http://localhost:8000)
- Documentación Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- Documentación ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- Base de datos (PostgreSQL): puerto local `5433`
- Redis: puerto local `6379`

---

# Ejecución local con Python (sin Docker)

Si prefieres ejecutar la aplicación directamente desde tu entorno local, debes configurar tu entorno virtual y asegurarte de que las variables de entorno `.env` apunten a **tus servicios reales** (no los contenedores).

---

## 1. Crear entorno virtual

### En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### En Linux o Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 3. Configurar variables de entorno

Crea un archivo `.env` (puedes copiar el ejemplo si existe):

```bash
cp .env.example .env
```

Edita las variables con tus configuraciones reales (base de datos y Redis):

```bash
DB_TYPE=postgres
DB_USER=admin
DB_PASSWORD=admin123
DB_NAME=appcine
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/0

SECRET_KEY=super_secret_key_123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=200

FRONTEND_ORIGIN=http://localhost:3000
```

> **Importante:**  
> Si ejecutas el proyecto localmente (sin Docker), debes reemplazar:
> - `DB_HOST=db` por el host real o `localhost` si usas una base de datos instalada localmente.  
> - `REDIS_URL=redis://redis:6379/0` por la URL de tu servidor Redis real (por ejemplo, `redis://localhost:6379/0` o un host remoto).  

Ejemplo para ejecución local real:
```bash
DB_HOST=localhost
REDIS_URL=redis://localhost:6379/0
```

---

## 4. Ejecutar la aplicación localmente
```bash
uvicorn app.main:app --reload
```

La aplicación se ejecutará en:
```
http://localhost:8000
```

---

## 5. Ver documentación

- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 6. Detener el entorno virtual
```bash
deactivate
```
