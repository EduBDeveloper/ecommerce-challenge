import httpx
from app.settings import settings


async def get_inventory_for_product(product_id: int):
    """
    Consulta el inventario externo para un producto dado.
    Retorna el inventario como JSON o None si falla la consulta.
    """
    if not settings.INVENTORY_API_URL:
        return {"error": "INVENTORY_API_URL no está definida"}

    url = f"{settings.INVENTORY_API_URL}/{product_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return None
        return response.json()
