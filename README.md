# E-commerce Challenge

**Proyecto Backend en FastAPI**

Este proyecto es una prueba técnica para un puesto de desarrollador backend en un banco. Implementa un sistema de e-commerce con funcionalidades de usuarios, API Keys, clientes, productos, pedidos, integración con RabbitMQ y un cliente HTTP externo para inventario.

---

## 📁 Estructura del proyecto

```
├── app/
│   ├── auth.py             # Lógica de JWT (create_access_token, SECRET_KEY, ALGORITHM)
│   ├── crud.py             # Operaciones CRUD y lógica de negocio
│   ├── dependencies.py     # Dependencias de FastAPI (DB, autenticación, API Key)
│   ├── external.py         # Cliente httpx para inventario externo
│   ├── main.py             # Configuración de FastAPI, routers y eventos
│   ├── models.py           # Modelos SQLAlchemy y session async
│   ├── queue.py            # Publicación en RabbitMQ
│   ├── routers/
│   │   ├── auth.py         # Login (JWT)
│   │   ├── user.py         # Registro de usuario y generación de API Key
│   │   ├── customer.py     # Gestión de clientes
│   │   ├── product.py      # Gestión de productos e inventario externo
│   │   └── order.py        # Gestión de pedidos
│   ├── schemas.py          # Pydantic schemas y validaciones con @field_validator
│   └── settings.py         # Carga de .env, configuración y entornos
│
├── tests/                  # Tests unitarios con pytest
│   ├── test_api.py
│   ├── test_auth.py
│   ├── test_crud.py
│   ├── test_external.py
│   ├── test_models.py
│   └── test_queue.py
│
├── Dockerfile              # Imagen de la aplicación Python
├── docker-compose.yml      # Servicios: app, db (Postgres), rabbitmq
├── requirements.txt        # Dependencias del proyecto
├── pytest.ini              # Configuración de pytest
└── README.md               # Este documento
```

---

## 🚀 Levantar el proyecto con Docker

> **Requisito**: Tener instalado Docker y Docker Compose.

1. Clona este repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd ecommerce-challenge
```

2. Construye y levanta los contenedores:

```bash
docker-compose up --build
```

* El servicio `db` (Postgres) correrá en el puerto `5432`.
* El servicio `rabbitmq` correrá en los puertos `5672` (AMQP) y `15672` (UI).
* La aplicación FastAPI correrá en el puerto `8000`.

3. Accede a la API en:

* **Swagger UI**: `http://localhost:8000/docs`
* **ReDoc**: `http://localhost:8000/redoc`

4. Para detener los contenedores:

```bash
docker-compose down
```

> **Nota**: No es necesario crear un archivo `.env` si se levanta con Docker, ya que las variables están definidas directamente en `docker-compose.yml` bajo `environment:`. El `.env` actual solo contiene:
>
> ```env
> DATABASE_URL=postgresql+asyncpg://postgres:1234@db:5432/ecommerce
> INVENTORY_API_URL=https://fakestoreapi.com/products
> ENV=development
> ```

---

## 🛠️ Instalación y ejecución local (sin Docker)

> **Requisito**: Python 3.11+ instalado.

1. Clona este repositorio y crea un entorno virtual:

```bash
git clone <URL_DEL_REPOSITORIO>
cd ecommerce-challenge
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

2. Instala dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Copia el archivo de ejemplo de variables de entorno y edítalo:

```bash
cp .env.example .env
```

Ajusta las variables según tu entorno:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:1234@localhost:5432/ecommerce
INVENTORY_API_URL=https://fakestoreapi.com/products
ENV=development
```

4. Crea la base de datos local (si aún no existe):

```bash
psql -U postgres -c "CREATE DATABASE ecommerce;"
```

5. Levanta la aplicación:

```bash
uvicorn app.main:app --reload
```

6. Verifica que corra en `http://localhost:8000`.

---

## ✅ Ejecutar pruebas (pytest)

Con Docker:

```bash
docker-compose exec app pytest -v
```

Sin Docker (entorno local activo):

```bash
pytest -v
```

Todas las pruebas unitarias se encuentran en la carpeta `tests/` y cubren:

* Autenticación JWT
* CRUD de usuarios, productos, clientes y órdenes
* Colas RabbitMQ (mock)
* Consumo de API externa (mock)

---

## 🔐 Autenticación y uso de la API

1. **Registro de usuario**:

* `POST /users/`
  Request JSON: `{ "username": "usuario1", "password": "secret123" }`
  Response: `{ "id": 1, "username": "usuario1" }`

2. **Generar API Key**:

* `POST /users/{user_id}/api-key`
  Header: `Authorization: Bearer <token>`
  Response: `{ "id": 1, "key": "<api_key>" }`

3. **Login (JWT)**:

* `POST /auth/login`
  Form data: `username`, `password`
  Response: `{ "access_token": "<jwt>", "token_type": "bearer" }`

4. **Rutas protegidas** (necesitan JWT + API Key en header):

* `POST /customers/`
* `POST /products/`
* `POST /orders/`

Debe incluir:

```http
Authorization: Bearer <jwt>
X-API-Key: <api_key>
```

5. **Rutas públicas**:

* `GET /customers/{id}`
* `GET /products/`
* `GET /products/{id}` (consulta inventario externo)
* `GET /orders/{id}`

---

## 📚 Documentación automática

FastAPI genera documentación interactiva basada en los docstrings y los schemas:

* **Swagger UI**: `http://localhost:8000/docs`
* **ReDoc**: `http://localhost:8000/redoc`

Ahí encontrarás ejemplos de request/response, modelos de datos y la descripción de cada endpoint.

---

## 👏 Cierre

Este proyecto fue diseñado aplicando los principios SOLID (SRP, OCP, LSP, ISP y DIP) para garantizar un código limpio, modular y mantenible.

¡Gracias por revisar mi prueba técnica! Estoy a disposición para cualquier consulta o demo adicional.
