# Imagen base con Python
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de tu proyecto al contenedor
COPY . .

# Instalar las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Exponer el puerto de la aplicación (por defecto FastAPI usa 8000)
EXPOSE 8000

# Comando para correr la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
