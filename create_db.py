import asyncio
from app.models import Base, engine

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 
        await conn.run_sync(Base.metadata.create_all)
        print("Tablas creadas correctamente.")

if __name__ == "__main__":
    asyncio.run(init_models())
