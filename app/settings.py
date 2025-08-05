from dotenv import load_dotenv
import os

# Cargar .env desde la raíz del proyecto
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class Settings:
    ENV = os.getenv("ENV", "development").lower()
    TESTING = ENV == "testing"
    DEVELOPMENT = ENV == "development"

    SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1234@localhost:5432/ecommerce")

    if not TESTING:
        RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
        RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
        RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
        RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
        RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "order_queue")
        RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
        INVENTORY_API_URL = os.getenv("INVENTORY_API_URL", "https://fakestoreapi.com/products")
    else:
        RABBITMQ_HOST = None
        RABBITMQ_PORT = None
        RABBITMQ_USER = None
        RABBITMQ_PASSWORD = None
        RABBITMQ_QUEUE = None
        RABBITMQ_URL = None
        INVENTORY_API_URL = None

settings = Settings()

#para debug:
print(f"ENV={settings.ENV}")
print(f"TESTING={settings.TESTING}")
print(f"INVENTORY_API_URL={settings.INVENTORY_API_URL}")
